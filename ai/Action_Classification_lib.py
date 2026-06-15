import cv2
import numpy as np
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class ActionClassificationConfig:
    image_size: int = 224
    crop_margin: float = 0.15
    topk: int = 3
    classify_only_holding: bool = True
    classify_actions: Tuple[str, ...] = ("Pick", "Work")
    device: Optional[str] = None
    draw_result: bool = True
    font_scale: float = 0.65
    line_thickness: int = 2


def get_device(device=None):
    if device is not None:
        return device

    return "cuda" if torch.cuda.is_available() else "cpu"


def box_xyxy(box):
    x1, y1, x2, y2 = map(float, box)

    if x2 < x1:
        x1, x2 = x2, x1

    if y2 < y1:
        y1, y2 = y2, y1

    return x1, y1, x2, y2


def box_area(box):
    x1, y1, x2, y2 = box_xyxy(box)
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def box_center(box):
    x1, y1, x2, y2 = box_xyxy(box)
    return (x1 + x2) * 0.5, (y1 + y2) * 0.5


def center_distance(box_a, box_b):
    ax, ay = box_center(box_a)
    bx, by = box_center(box_b)

    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5


def expand_box(box, margin, image_w, image_h):
    x1, y1, x2, y2 = box_xyxy(box)

    w = x2 - x1
    h = y2 - y1

    nx1 = max(0.0, x1 - w * margin)
    ny1 = max(0.0, y1 - h * margin)
    nx2 = min(float(image_w - 1), x2 + w * margin)
    ny2 = min(float(image_h - 1), y2 + h * margin)

    return nx1, ny1, nx2, ny2


def crop_from_box(frame, box, margin=0.0):
    if frame is None:
        return None

    h, w = frame.shape[:2]
    x1, y1, x2, y2 = expand_box(box, margin, w, h)

    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))

    x1 = max(0, min(w - 1, x1))
    y1 = max(0, min(h - 1, y1))
    x2 = max(0, min(w, x2))
    y2 = max(0, min(h, y2))

    if x2 <= x1 or y2 <= y1:
        return None

    return frame[y1:y2, x1:x2].copy()


def normalize_state_dict_keys(state_dict):
    fixed = {}

    for key, value in state_dict.items():
        new_key = key

        if new_key.startswith("module."):
            new_key = new_key[len("module."):]

        if new_key.startswith("model."):
            new_key = new_key[len("model."):]

        fixed[new_key] = value

    return fixed


def build_resnet18(num_classes):
    from torchvision.models import resnet18

    model = resnet18(weights=None)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, int(num_classes))

    return model


def load_resnet18_classifier(model_path, num_classes, device):
    model = build_resnet18(num_classes=num_classes)

    ckpt = torch.load(model_path, map_location=device)

    if isinstance(ckpt, dict):
        if "model_state_dict" in ckpt:
            state_dict = ckpt["model_state_dict"]
        elif "model_state" in ckpt:
            state_dict = ckpt["model_state"]
        elif "state_dict" in ckpt:
            state_dict = ckpt["state_dict"]
        else:
            state_dict = ckpt
    else:
        state_dict = ckpt

    state_dict = normalize_state_dict_keys(state_dict)
    model.load_state_dict(state_dict, strict=True)
    model.to(device)
    model.eval()

    return model


def preprocess_crop(crop, image_size, device):
    if crop is None or crop.size == 0:
        return None

    crop = cv2.resize(crop, (image_size, image_size), interpolation=cv2.INTER_LINEAR)
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    arr = crop.astype(np.float32) / 255.0

    tensor = torch.from_numpy(arr).permute(2, 0, 1).contiguous().float()

    mean = torch.tensor([0.485, 0.456, 0.406], dtype=torch.float32).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225], dtype=torch.float32).view(3, 1, 1)

    tensor = (tensor - mean) / std
    tensor = tensor.unsqueeze(0).to(device)

    return tensor


def find_track_by_id(action_yolo_result, track_id):
    track_id = int(track_id)

    for track in action_yolo_result.get("tracks", []):
        if int(track.get("track_id", -1)) == track_id:
            return track

    return None


def select_product_from_track(track):
    products = track.get("products", [])
    hands = track.get("hands", [])

    if len(products) == 0:
        return None

    if len(hands) > 0:
        best_product = None
        best_dist = 999999.0

        for product in products:
            pbox = product.get("box", None)

            if pbox is None:
                continue

            for hand in hands:
                hbox = hand.get("box", None)

                if hbox is None:
                    continue

                dist = center_distance(pbox, hbox)

                if dist < best_dist:
                    best_dist = dist
                    best_product = product

        if best_product is not None:
            return best_product

    best_product = None
    best_score = -1.0

    for product in products:
        pbox = product.get("box", None)

        if pbox is None:
            continue

        conf = float(product.get("conf", 0.0))
        area = box_area(pbox)
        score = area * max(conf, 0.01)

        if score > best_score:
            best_score = score
            best_product = product

    return best_product


def should_classify_person(person, config):
    action = str(person.get("action", ""))
    holding = bool(person.get("holding", False))

    if config.classify_only_holding:
        if holding:
            return True

        if action in config.classify_actions:
            return True

        return False

    return True


def draw_classification(frame, product_box, text, color, config):
    x1, y1, x2, y2 = [int(round(v)) for v in box_xyxy(product_box)]

    h, w = frame.shape[:2]

    x1 = max(0, min(w - 1, x1))
    y1 = max(0, min(h - 1, y1))
    x2 = max(0, min(w - 1, x2))
    y2 = max(0, min(h - 1, y2))

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        config.line_thickness,
    )

    cv2.putText(
        frame,
        text,
        (x1, max(20, y1 - 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        config.font_scale,
        color,
        config.line_thickness,
        cv2.LINE_AA,
    )


class ActionProductClassifier:
    def __init__(self, model_path, class_names, config=None):
        self.config = config if config is not None else ActionClassificationConfig()
        self.device = get_device(self.config.device)
        self.class_names = list(class_names)
        self.num_classes = len(self.class_names)

        if self.num_classes <= 0:
            raise ValueError("class_names must have at least one class")

        self.model = load_resnet18_classifier(
            model_path=model_path,
            num_classes=self.num_classes,
            device=self.device,
        )

    def classify_crop(self, crop):
        tensor = preprocess_crop(
            crop=crop,
            image_size=self.config.image_size,
            device=self.device,
        )

        if tensor is None:
            return None

        with torch.no_grad():
            logits = self.model(tensor)
            probs = F.softmax(logits, dim=1)[0]

        topk = min(int(self.config.topk), self.num_classes)
        values, indices = torch.topk(probs, k=topk)

        topk_rows = []

        for value, index in zip(values.detach().cpu().tolist(), indices.detach().cpu().tolist()):
            index = int(index)
            topk_rows.append({
                "class_id": index,
                "class_name": self.class_names[index],
                "prob": round(float(value), 4),
            })

        best = topk_rows[0]

        return {
            "class_id": best["class_id"],
            "class_name": best["class_name"],
            "prob": best["prob"],
            "topk": topk_rows,
        }

    def process(self, frame, action_result, action_yolo_result, debug=False, draw_frame=None):
        if frame is None:
            return {
                "cam_id": action_result.get("cam_id", -1) if action_result is not None else -1,
                "frame_idx": action_result.get("frame_idx", -1) if action_result is not None else -1,
                "classifications": [],
                "count": {"classified": 0},
            }, None

        if action_result is None or action_yolo_result is None:
            return {
                "cam_id": -1,
                "frame_idx": -1,
                "classifications": [],
                "count": {"classified": 0},
            }, None

        output_frame = None

        if debug:
            if draw_frame is not None:
                output_frame = draw_frame.copy()
            else:
                output_frame = frame.copy()

        cam_id = int(action_result.get("cam_id", action_yolo_result.get("cam_id", -1)))
        frame_idx = int(action_result.get("frame_idx", action_yolo_result.get("frame_idx", -1)))

        rows = []

        for person in action_result.get("persons", []):
            if not should_classify_person(person, self.config):
                continue

            track_id = int(person.get("track_id", -1))

            if track_id < 0:
                continue

            track = find_track_by_id(
                action_yolo_result=action_yolo_result,
                track_id=track_id,
            )

            if track is None:
                continue

            product = select_product_from_track(track)

            if product is None:
                continue

            product_box = product.get("box", None)

            if product_box is None:
                continue

            crop = crop_from_box(
                frame=frame,
                box=product_box,
                margin=self.config.crop_margin,
            )

            pred = self.classify_crop(crop)

            if pred is None:
                continue

            row = {
                "cam_id": cam_id,
                "frame_idx": frame_idx,
                "track_id": track_id,
                "topview_person_id": int(track.get("topview_person_id", -1)),
                "action": person.get("action", ""),
                "holding": bool(person.get("holding", False)),
                "product_box": [round(float(v), 2) for v in box_xyxy(product_box)],
                "product_conf": round(float(product.get("conf", 0.0)), 4),
                "class_id": int(pred["class_id"]),
                "class_name": str(pred["class_name"]),
                "prob": round(float(pred["prob"]), 4),
                "topk": pred["topk"],
            }

            rows.append(row)

            if output_frame is not None and self.config.draw_result:
                label = f"{row['class_name']} {row['prob']:.2f}"
                color = (0, 255, 255)

                draw_classification(
                    frame=output_frame,
                    product_box=product_box,
                    text=label,
                    color=color,
                    config=self.config,
                )

        result = {
            "cam_id": cam_id,
            "frame_idx": frame_idx,
            "classifications": rows,
            "count": {
                "classified": len(rows),
            },
        }

        return result, output_frame


def create_action_classifier(model_path, class_names, config=None):
    return ActionProductClassifier(
        model_path=model_path,
        class_names=class_names,
        config=config,
    )


def classify_action_products(manager, frame, action_result, action_yolo_result, debug=False, draw_frame=None):
    return manager.process(
        frame=frame,
        action_result=action_result,
        action_yolo_result=action_yolo_result,
        debug=debug,
        draw_frame=draw_frame,
    )