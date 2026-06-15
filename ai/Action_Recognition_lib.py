import cv2
import math
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Tuple

from YOLO_lib import box_xyxy, box_center, box_wh, box_iou, compute_containment, center_distance


@dataclass
class ActionRecognitionConfig:
    close_dist_norm: float = 0.45
    close_iou_thres: float = 0.01
    close_contain_thres: float = 0.10
    pick_confirm_frames: int = 3
    place_confirm_frames: int = 5
    min_hold_frames: int = 8
    event_display_frames: int = 15
    max_missing_frames: int = 30
    font_scale: float = 0.7
    line_thickness: int = 2
    draw_box: bool = True


@dataclass
class ActionTrackState:
    track_id: int
    last_box: Tuple[float, float, float, float] = None
    last_center: Tuple[float, float] = None
    last_frame_idx: int = 0
    missing_frames: int = 0
    holding: bool = False
    hold_frames: int = 0
    close_streak: int = 0
    no_close_streak: int = 0
    event_label: str = ""
    event_remain: int = 0
    last_action: str = "other_work"


def safe_get_box(item):
    if item is None:
        return None

    box = item.get("box", None)

    if box is None:
        return None

    return box_xyxy(box)


def min_hand_product_distance_norm(hands, products, person_box):
    if len(hands) == 0 or len(products) == 0:
        return 999.0

    pw, ph = box_wh(person_box)
    diag = math.sqrt(pw * pw + ph * ph)
    diag = max(diag, 1.0)

    min_dist = 999.0

    for hand in hands:
        hbox = safe_get_box(hand)

        if hbox is None:
            continue

        for product in products:
            pbox = safe_get_box(product)

            if pbox is None:
                continue

            dist = center_distance(hbox, pbox) / diag

            if dist < min_dist:
                min_dist = dist

    return float(min_dist)


def is_hand_product_close(hands, products, person_box, config):
    if len(hands) == 0 or len(products) == 0:
        return False, 999.0

    pw, ph = box_wh(person_box)
    diag = math.sqrt(pw * pw + ph * ph)
    diag = max(diag, 1.0)

    best_dist = 999.0
    close = False

    for hand in hands:
        hbox = safe_get_box(hand)

        if hbox is None:
            continue

        for product in products:
            pbox = safe_get_box(product)

            if pbox is None:
                continue

            dist_norm = center_distance(hbox, pbox) / diag
            iou = box_iou(hbox, pbox)
            contain = compute_containment(hbox, pbox)

            if dist_norm < best_dist:
                best_dist = dist_norm

            if dist_norm <= config.close_dist_norm:
                close = True

            if iou >= config.close_iou_thres:
                close = True

            if contain >= config.close_contain_thres:
                close = True

    return close, float(best_dist)


def estimate_motion_norm(state, person_box):
    cx, cy = box_center(person_box)

    if state.last_center is None:
        return 0.0

    lx, ly = state.last_center
    pw, ph = box_wh(person_box)
    diag = math.sqrt(pw * pw + ph * ph)
    diag = max(diag, 1.0)

    return math.sqrt((cx - lx) ** 2 + (cy - ly) ** 2) / diag


def action_color(action):
    if action == "Pick":
        return (0, 255, 0)

    if action == "Place":
        return (0, 160, 255)

    if action == "Work":
        return (255, 255, 0)

    return (180, 180, 180)


def draw_action_label(frame, box, label, color, config):
    x1, y1, x2, y2 = [int(round(v)) for v in box_xyxy(box)]

    h, w = frame.shape[:2]

    x1 = max(0, min(w - 1, x1))
    y1 = max(0, min(h - 1, y1))
    x2 = max(0, min(w - 1, x2))
    y2 = max(0, min(h - 1, y2))

    if config.draw_box:
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, config.line_thickness)

    cv2.putText(
        frame,
        label,
        (x1, min(h - 10, y2 + 25)),
        cv2.FONT_HERSHEY_SIMPLEX,
        config.font_scale,
        color,
        config.line_thickness,
        cv2.LINE_AA,
    )


class ActionRecognitionManager:
    def __init__(self, num_cctv=8, config=None):
        self.num_cctv = int(num_cctv)
        self.config = config if config is not None else ActionRecognitionConfig()
        self.states = {}

        for cam_id in range(self.num_cctv):
            self.states[int(cam_id)] = {}

    def reset_camera(self, cam_id):
        cam_id = int(cam_id)
        self.states[cam_id] = {}

    def get_state(self, cam_id, track_id):
        cam_id = int(cam_id)
        track_id = int(track_id)

        if cam_id not in self.states:
            self.states[cam_id] = {}

        if track_id not in self.states[cam_id]:
            self.states[cam_id][track_id] = ActionTrackState(track_id=track_id)

        return self.states[cam_id][track_id]

    def remove_old_states(self, cam_id, seen_track_ids):
        cam_id = int(cam_id)
        seen_track_ids = set(int(x) for x in seen_track_ids)

        delete_ids = []

        for track_id, state in self.states[cam_id].items():
            if int(track_id) not in seen_track_ids:
                state.missing_frames += 1

            if state.missing_frames > self.config.max_missing_frames:
                delete_ids.append(track_id)

        for track_id in delete_ids:
            del self.states[cam_id][track_id]

    def process(self, yolo_result, frame=None, cam_id=None, debug=False):
        if yolo_result is None:
            return {
                "cam_id": cam_id,
                "frame_idx": -1,
                "persons": [],
                "count": {},
            }, None

        if cam_id is None:
            cam_id = int(yolo_result.get("cam_id", 0))

        cam_id = int(cam_id)
        frame_idx = int(yolo_result.get("frame_idx", 0))
        tracks = yolo_result.get("tracks", [])

        persons = []
        seen_track_ids = []

        output_frame = None

        if debug and frame is not None:
            output_frame = frame.copy()

        for track in tracks:
            track_id = int(track.get("track_id", -1))

            if track_id < 0:
                continue

            person_box = safe_get_box(track)

            if person_box is None:
                continue

            seen_track_ids.append(track_id)

            hands = track.get("hands", [])
            hats = track.get("hats", [])
            products = track.get("products", [])

            state = self.get_state(cam_id, track_id)
            state.missing_frames = 0

            close, min_dist_norm = is_hand_product_close(
                hands=hands,
                products=products,
                person_box=person_box,
                config=self.config,
            )

            motion_norm = estimate_motion_norm(state, person_box)
            has_hand = len(hands) > 0
            has_product = len(products) > 0
            work_candidate = has_hand and has_product and close

            event = ""

            if work_candidate:
                state.close_streak += 1
                state.no_close_streak = 0
            else:
                state.close_streak = 0
                state.no_close_streak += 1

            if state.holding:
                state.hold_frames += 1
            else:
                state.hold_frames = 0

            if work_candidate and not state.holding and state.close_streak >= self.config.pick_confirm_frames:
                event = "Pick"
                state.holding = True
                state.hold_frames = 0
                state.event_label = "Pick"
                state.event_remain = self.config.event_display_frames

            elif state.holding and state.no_close_streak >= self.config.place_confirm_frames and state.hold_frames >= self.config.min_hold_frames:
                event = "Place"
                state.holding = False
                state.hold_frames = 0
                state.event_label = "Place"
                state.event_remain = self.config.event_display_frames

            if state.event_remain > 0:
                action = state.event_label
                state.event_remain -= 1
            else:
                if work_candidate or state.holding:
                    action = "Work"
                else:
                    action = "other_work"

            score = 0.0

            if has_hand:
                score += 0.25

            if has_product:
                score += 0.25

            if close:
                score += 0.35

            score += min(motion_norm, 0.30) * 0.50
            score = min(1.0, float(score))

            cx, cy = box_center(person_box)

            state.last_box = person_box
            state.last_center = (cx, cy)
            state.last_frame_idx = frame_idx
            state.last_action = action

            person_row = {
                "cam_id": cam_id,
                "frame_idx": frame_idx,
                "track_id": track_id,
                "action": action,
                "event": event,
                "score": round(score, 4),
                "holding": bool(state.holding),
                "box": [round(float(v), 2) for v in person_box],
                "hand_count": len(hands),
                "hat_count": len(hats),
                "product_count": len(products),
                "close_hand_product": bool(close),
                "min_hand_product_dist_norm": round(float(min_dist_norm), 4),
                "motion_norm": round(float(motion_norm), 4),
                "close_streak": int(state.close_streak),
                "no_close_streak": int(state.no_close_streak),
                "hold_frames": int(state.hold_frames),
            }

            persons.append(person_row)

            if output_frame is not None:
                color = action_color(action)
                label = f"ID{track_id} {action} {score:.2f}"

                if event != "":
                    label = f"ID{track_id} EVENT:{event}"

                draw_action_label(
                    frame=output_frame,
                    box=person_box,
                    label=label,
                    color=color,
                    config=self.config,
                )

        self.remove_old_states(cam_id, seen_track_ids)

        count = {
            "person": len(persons),
            "other_work": sum(1 for x in persons if x["action"] == "other_work"),
            "work": sum(1 for x in persons if x["action"] == "Work"),
            "pick": sum(1 for x in persons if x["action"] == "Pick"),
            "place": sum(1 for x in persons if x["action"] == "Place"),
            "holding": sum(1 for x in persons if x["holding"]),
        }

        result = {
            "cam_id": cam_id,
            "frame_idx": frame_idx,
            "persons": persons,
            "count": count,
        }

        return result, output_frame


def create_action_recognizer(num_cctv=8, config=None):
    return ActionRecognitionManager(
        num_cctv=num_cctv,
        config=config,
    )


def recognize_action(manager, yolo_result, frame=None, cam_id=None, debug=False):
    return manager.process(
        yolo_result=yolo_result,
        frame=frame,
        cam_id=cam_id,
        debug=debug,
    )