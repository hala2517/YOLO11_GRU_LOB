import cv2
import math
import numpy as np
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass
class YOLOTrackConfig:
    device: Any = 0
    imgsz: int = 640
    conf: float = 0.20
    iou: float = 0.45
    max_det: int = 2000
    person_class_ids: Tuple[int, ...] = (0,)
    hand_class_ids: Tuple[int, ...] = (1,)
    hat_class_ids: Tuple[int, ...] = (2,)
    product_class_ids: Tuple[int, ...] = (3,)
    min_conf_by_class: Dict[int, float] = field(default_factory=lambda: {
        0: 0.30,
        1: 0.20,
        2: 0.20,
        3: 0.20,
    })
    min_area_by_class: Dict[int, float] = field(default_factory=lambda: {
        0: 800,
        1: 60,
        2: 60,
        3: 40,
    })
    enable_dedup: bool = True
    track_iou_threshold: float = 0.25
    track_max_center_dist: float = 180.0
    track_max_missing: int = 30
    track_min_conf: float = 0.30
    hand_expand_x: float = 0.35
    hand_expand_y: float = 0.35
    hat_expand_x: float = 0.25
    hat_expand_y: float = 0.15
    product_expand_x: float = 0.50
    product_expand_y: float = 0.50
    draw_person_track: bool = True
    draw_hand: bool = True
    draw_hat: bool = True
    draw_product: bool = True
    draw_relation: bool = True
    font_scale: float = 0.6
    line_thickness: int = 2


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


def box_wh(box):
    x1, y1, x2, y2 = box_xyxy(box)
    return max(1.0, x2 - x1), max(1.0, y2 - y1)


def box_iou(a, b):
    ax1, ay1, ax2, ay2 = box_xyxy(a)
    bx1, by1, bx2, by2 = box_xyxy(b)

    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)

    iw = max(0.0, ix2 - ix1)
    ih = max(0.0, iy2 - iy1)

    inter = iw * ih
    union = box_area(a) + box_area(b) - inter

    if union <= 1e-9:
        return 0.0

    return inter / union


def center_distance(a, b):
    ax, ay = box_center(a)
    bx, by = box_center(b)
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def compute_containment(a, b):
    ax1, ay1, ax2, ay2 = box_xyxy(a)
    bx1, by1, bx2, by2 = box_xyxy(b)

    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)

    iw = max(0.0, ix2 - ix1)
    ih = max(0.0, iy2 - iy1)

    inter = iw * ih
    small = max(1.0, min(box_area(a), box_area(b)))

    return inter / small


def expanded_box(box, sx, sy, image_w, image_h):
    x1, y1, x2, y2 = box_xyxy(box)

    w = x2 - x1
    h = y2 - y1

    return (
        max(0.0, x1 - w * sx),
        max(0.0, y1 - h * sy),
        min(float(image_w - 1), x2 + w * sx),
        min(float(image_h - 1), y2 + h * sy),
    )


def point_in_box(x, y, box):
    x1, y1, x2, y2 = box_xyxy(box)
    return x1 <= x <= x2 and y1 <= y <= y2


def normalize_yolo_names(names):
    if isinstance(names, dict):
        return names

    if isinstance(names, list):
        return {i: name for i, name in enumerate(names)}

    return {}


def class_name_from_id(names, cls_id):
    names = normalize_yolo_names(names)
    return str(names.get(int(cls_id), str(cls_id)))


def get_min_conf(cls_id, config):
    return float(config.min_conf_by_class.get(int(cls_id), 0.20))


def get_min_area(cls_id, config):
    return float(config.min_area_by_class.get(int(cls_id), 40))


def is_duplicate_box(box_a, box_b, cls_id):
    iou = box_iou(box_a, box_b)
    contain = compute_containment(box_a, box_b)

    cls_id = int(cls_id)

    if cls_id == 0:
        return iou >= 0.60 or contain >= 0.85

    if cls_id == 1:
        return iou >= 0.55 or contain >= 0.85

    if cls_id == 2:
        return iou >= 0.55 or contain >= 0.85

    if cls_id == 3:
        return iou >= 0.65 or contain >= 0.90

    return iou >= 0.60 or contain >= 0.90


def dedup_dets(dets):
    if not dets:
        return []

    order = sorted(
        range(len(dets)),
        key=lambda i: float(dets[i]["conf"]),
        reverse=True,
    )

    kept = []

    for idx in order:
        d = dets[idx]
        duplicated = False

        for kd in kept:
            if int(kd["cls"]) != int(d["cls"]):
                continue

            if is_duplicate_box(kd["box"], d["box"], d["cls"]):
                duplicated = True
                break

        if not duplicated:
            kept.append(d)

    return kept


def parse_yolo_predict_result(result, names, config):
    dets = []

    target_ids = (
        set(config.person_class_ids)
        | set(config.hand_class_ids)
        | set(config.hat_class_ids)
        | set(config.product_class_ids)
    )

    if result is None or result.boxes is None or len(result.boxes) == 0:
        return [], [], [], [], []

    xyxy = result.boxes.xyxy.detach().cpu().numpy()
    conf = result.boxes.conf.detach().cpu().numpy()
    cls = result.boxes.cls.detach().cpu().numpy().astype(int)

    for b, cf, c in zip(xyxy, conf, cls):
        c = int(c)
        cf = float(cf)

        if c not in target_ids:
            continue

        if cf < get_min_conf(c, config):
            continue

        box = box_xyxy(tuple(map(float, b.tolist())))

        if box_area(box) < get_min_area(c, config):
            continue

        dets.append({
            "box": box,
            "conf": cf,
            "cls": c,
            "cls_name": class_name_from_id(names, c),
        })

    if config.enable_dedup:
        dets = dedup_dets(dets)

    person_dets = []
    hand_dets = []
    hat_dets = []
    product_dets = []

    person_set = set(config.person_class_ids)
    hand_set = set(config.hand_class_ids)
    hat_set = set(config.hat_class_ids)
    product_set = set(config.product_class_ids)

    for det in dets:
        cls_id = int(det["cls"])

        if cls_id in person_set:
            person_dets.append(det)
        elif cls_id in hand_set:
            hand_dets.append(det)
        elif cls_id in hat_set:
            hat_dets.append(det)
        elif cls_id in product_set:
            product_dets.append(det)

    return dets, person_dets, hand_dets, hat_dets, product_dets


def infer_one_frame_yolo(model, frame, config):
    names = normalize_yolo_names(getattr(model, "names", {}))

    try:
        predict_kwargs = {
            "source": frame,
            "imgsz": config.imgsz,
            "conf": config.conf,
            "iou": config.iou,
            "max_det": config.max_det,
            "verbose": False,
        }

        if config.device is not None:
            predict_kwargs["device"] = config.device

        results = model.predict(**predict_kwargs)
        result = results[0] if results else None

    except Exception as e:
        print(f"[YOLO WARN] predict fail: {e}")
        result = None

    return parse_yolo_predict_result(result, names, config)


@dataclass
class Track:
    track_id: int
    box: Tuple[float, float, float, float]
    conf: float
    last_frame: int
    missing: int = 0


class SimplePersonTracker:
    def __init__(self, config=None):
        self.config = config if config is not None else YOLOTrackConfig()
        self.tracks: Dict[int, Track] = {}
        self.next_id = 1

    def update(self, person_dets: List[Dict[str, Any]], frame_idx: int) -> List[Track]:
        detections = [
            det for det in person_dets
            if float(det.get("conf", 0.0)) >= self.config.track_min_conf
        ]

        assigned_det = set()
        assigned_track = set()
        track_ids = list(self.tracks.keys())
        pairs = []

        for tid in track_ids:
            track = self.tracks[tid]

            for det_idx, det in enumerate(detections):
                iou = box_iou(track.box, det["box"])
                dist = center_distance(track.box, det["box"])
                score = iou * 3.0 - dist / max(self.config.track_max_center_dist, 1.0)

                if iou >= self.config.track_iou_threshold or dist <= self.config.track_max_center_dist:
                    pairs.append((score, tid, det_idx))

        pairs.sort(reverse=True, key=lambda x: x[0])

        for score, tid, det_idx in pairs:
            if tid in assigned_track or det_idx in assigned_det:
                continue

            track = self.tracks[tid]
            det = detections[det_idx]

            track.box = box_xyxy(det["box"])
            track.conf = float(det.get("conf", 0.0))
            track.last_frame = int(frame_idx)
            track.missing = 0

            assigned_track.add(tid)
            assigned_det.add(det_idx)

        for det_idx, det in enumerate(detections):
            if det_idx in assigned_det:
                continue

            tid = self.next_id
            self.next_id += 1

            self.tracks[tid] = Track(
                track_id=tid,
                box=box_xyxy(det["box"]),
                conf=float(det.get("conf", 0.0)),
                last_frame=int(frame_idx),
            )

        dead = []

        for tid, track in self.tracks.items():
            if track.last_frame != frame_idx:
                track.missing += 1

            if track.missing > self.config.track_max_missing:
                dead.append(tid)

        for tid in dead:
            del self.tracks[tid]

        return [track for track in self.tracks.values() if track.missing == 0]


def assign_dets_to_tracks(tracks, dets, frame_w, frame_h, expand_x=0.35, expand_y=0.35):
    assigned = {int(track.track_id): [] for track in tracks}

    for det in dets:
        dbox = det["box"]
        dcx, dcy = box_center(dbox)

        best_track = None
        best_score = -1e9

        for track in tracks:
            search_box = expanded_box(
                track.box,
                expand_x,
                expand_y,
                frame_w,
                frame_h,
            )

            if not point_in_box(dcx, dcy, search_box):
                continue

            iou = box_iou(track.box, dbox)
            dist = center_distance(track.box, dbox)

            tw, th = box_wh(track.box)
            ref = max(tw, th, 1.0)

            score = iou * 2.0 + float(det["conf"]) - min(dist / ref, 2.0) * 0.2

            if score > best_score:
                best_score = score
                best_track = track

        if best_track is not None:
            assigned[int(best_track.track_id)].append(det)

    return assigned


def box_to_list(box):
    return [round(float(v), 2) for v in box_xyxy(box)]


def det_to_dict(det):
    return {
        "cls": int(det["cls"]),
        "cls_name": str(det["cls_name"]),
        "conf": round(float(det["conf"]), 4),
        "box": box_to_list(det["box"]),
    }


def track_to_dict(track, hand_items=None, hat_items=None, product_items=None):
    if hand_items is None:
        hand_items = []

    if hat_items is None:
        hat_items = []

    if product_items is None:
        product_items = []

    return {
        "track_id": int(track.track_id),
        "box": box_to_list(track.box),
        "conf": round(float(track.conf), 4),
        "missing": int(track.missing),
        "last_frame": int(track.last_frame),
        "hands": [det_to_dict(item) for item in hand_items],
        "hats": [det_to_dict(item) for item in hat_items],
        "products": [det_to_dict(item) for item in product_items],
    }


def color_for_id(track_id):
    rng = np.random.default_rng(int(track_id) * 9973)
    return tuple(int(x) for x in rng.integers(40, 230, size=3).tolist())


def draw_box_label(frame, box, label, color, thickness=2, font_scale=0.6):
    h, w = frame.shape[:2]
    x1, y1, x2, y2 = [int(round(v)) for v in box_xyxy(box)]

    x1 = max(0, min(w - 1, x1))
    y1 = max(0, min(h - 1, y1))
    x2 = max(0, min(w - 1, x2))
    y2 = max(0, min(h - 1, y2))

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

    if label:
        y_text = max(20, y1 - 6)

        cv2.putText(
            frame,
            label,
            (x1, y_text),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            color,
            max(1, thickness),
            cv2.LINE_AA,
        )


def draw_tracking_output(
    frame,
    cam_id,
    frame_idx,
    tracks,
    hand_by_track,
    hat_by_track,
    product_by_track,
    hand_dets,
    hat_dets,
    product_dets,
    config,
):
    vis = frame.copy()

    if config.draw_hand:
        for det in hand_dets:
            draw_box_label(
                vis,
                det["box"],
                f"hand {det['conf']:.2f}",
                (0, 255, 255),
                1,
                config.font_scale,
            )

    if config.draw_hat:
        for det in hat_dets:
            draw_box_label(
                vis,
                det["box"],
                f"hat {det['conf']:.2f}",
                (255, 0, 255),
                1,
                config.font_scale,
            )

    if config.draw_product:
        for det in product_dets:
            draw_box_label(
                vis,
                det["box"],
                f"prd {det['conf']:.2f}",
                (255, 180, 0),
                1,
                config.font_scale,
            )

    if config.draw_person_track:
        for track in tracks:
            color = color_for_id(track.track_id)

            hand_count = len(hand_by_track.get(int(track.track_id), []))
            hat_count = len(hat_by_track.get(int(track.track_id), []))
            product_count = len(product_by_track.get(int(track.track_id), []))

            label = (
                f"ID{track.track_id} "
                f"person {track.conf:.2f} "
                f"H:{hand_count} Hat:{hat_count} P:{product_count}"
            )

            draw_box_label(
                vis,
                track.box,
                label,
                color,
                config.line_thickness,
                config.font_scale,
            )

            if config.draw_relation:
                tcx, tcy = box_center(track.box)

                for det in hand_by_track.get(int(track.track_id), []):
                    dcx, dcy = box_center(det["box"])
                    cv2.line(
                        vis,
                        (int(tcx), int(tcy)),
                        (int(dcx), int(dcy)),
                        color,
                        1,
                        cv2.LINE_AA,
                    )

                for det in product_by_track.get(int(track.track_id), []):
                    dcx, dcy = box_center(det["box"])
                    cv2.line(
                        vis,
                        (int(tcx), int(tcy)),
                        (int(dcx), int(dcy)),
                        color,
                        1,
                        cv2.LINE_AA,
                    )

    info = (
        f"CAM {cam_id} | frame {frame_idx} | "
        f"tracks {len(tracks)} | "
        f"hand {len(hand_dets)} | hat {len(hat_dets)} | product {len(product_dets)}"
    )

    cv2.putText(
        vis,
        info,
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    return vis


class OneCCTVTrackState:
    def __init__(self, config=None):
        self.frame_idx = 0
        self.person_tracker = SimplePersonTracker(config=config)


class CCTVTrackYOLOManager:
    def __init__(self, model, num_cctv=8, config=None):
        self.model = model
        self.num_cctv = int(num_cctv)
        self.config = config if config is not None else YOLOTrackConfig()
        self.states = {}

        for cam_id in range(self.num_cctv):
            self.states[int(cam_id)] = OneCCTVTrackState(config=self.config)

    def reset_camera(self, cam_id):
        cam_id = int(cam_id)
        self.states[cam_id] = OneCCTVTrackState(config=self.config)

    def process_frame(self, frame, cam_id, debug=False):
        cam_id = int(cam_id)

        if cam_id not in self.states:
            raise ValueError(f"cam_id must be 0 ~ {self.num_cctv - 1}, got {cam_id}")

        state = self.states[cam_id]
        state.frame_idx += 1
        frame_idx = int(state.frame_idx)

        h, w = frame.shape[:2]

        (
            dets,
            person_dets,
            hand_dets,
            hat_dets,
            product_dets,
        ) = infer_one_frame_yolo(
            model=self.model,
            frame=frame,
            config=self.config,
        )

        tracks = state.person_tracker.update(
            person_dets=person_dets,
            frame_idx=frame_idx,
        )

        hand_by_track = assign_dets_to_tracks(
            tracks=tracks,
            dets=hand_dets,
            frame_w=w,
            frame_h=h,
            expand_x=self.config.hand_expand_x,
            expand_y=self.config.hand_expand_y,
        )

        hat_by_track = assign_dets_to_tracks(
            tracks=tracks,
            dets=hat_dets,
            frame_w=w,
            frame_h=h,
            expand_x=self.config.hat_expand_x,
            expand_y=self.config.hat_expand_y,
        )

        product_by_track = assign_dets_to_tracks(
            tracks=tracks,
            dets=product_dets,
            frame_w=w,
            frame_h=h,
            expand_x=self.config.product_expand_x,
            expand_y=self.config.product_expand_y,
        )

        track_rows = []

        for track in tracks:
            tid = int(track.track_id)

            track_rows.append(
                track_to_dict(
                    track=track,
                    hand_items=hand_by_track.get(tid, []),
                    hat_items=hat_by_track.get(tid, []),
                    product_items=product_by_track.get(tid, []),
                )
            )

        result = {
            "cam_id": cam_id,
            "frame_idx": frame_idx,
            "detections": {
                "all": [det_to_dict(item) for item in dets],
                "persons": [det_to_dict(item) for item in person_dets],
                "hands": [det_to_dict(item) for item in hand_dets],
                "hats": [det_to_dict(item) for item in hat_dets],
                "products": [det_to_dict(item) for item in product_dets],
            },
            "tracks": track_rows,
            "count": {
                "all_dets": len(dets),
                "person_dets": len(person_dets),
                "hand_dets": len(hand_dets),
                "hat_dets": len(hat_dets),
                "product_dets": len(product_dets),
                "person_tracks": len(tracks),
            },
        }

        output_frame = None

        if debug:
            output_frame = draw_tracking_output(
                frame=frame,
                cam_id=cam_id,
                frame_idx=frame_idx,
                tracks=tracks,
                hand_by_track=hand_by_track,
                hat_by_track=hat_by_track,
                product_by_track=product_by_track,
                hand_dets=hand_dets,
                hat_dets=hat_dets,
                product_dets=product_dets,
                config=self.config,
            )

        return result, output_frame


def create_yolo_tracker(model, num_cctv=8, config=None):
    manager = CCTVTrackYOLOManager(
        model=model,
        num_cctv=num_cctv,
        config=config,
    )

    return manager


def track_one_cctv_frame(manager, frame, cam_id, debug=False):
    result, output_frame = manager.process_frame(
        frame=frame,
        cam_id=cam_id,
        debug=debug,
    )

    return result, output_frame


def make_blank_frame(width=640, height=360, text="read fail"):
    blank = np.zeros((height, width, 3), dtype=np.uint8)

    cv2.putText(
        blank,
        text,
        (40, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )

    return blank


def make_8ch_grid(frames, view_w=640, view_h=360):
    show_frames = []

    for frame in frames:
        if frame is None:
            show = np.zeros((view_h, view_w, 3), dtype=np.uint8)
        else:
            show = cv2.resize(frame, (view_w, view_h))

        show_frames.append(show)

    while len(show_frames) < 8:
        show_frames.append(np.zeros((view_h, view_w, 3), dtype=np.uint8))

    row1 = np.hstack(show_frames[0:4])
    row2 = np.hstack(show_frames[4:8])
    grid = np.vstack([row1, row2])

    return grid