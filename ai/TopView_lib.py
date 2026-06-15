import cv2
import json
import math
import numpy as np
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

try:
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False


@dataclass
class TopViewConfig:
    annotation_json_path: str
    cam_id_to_ch: Dict[int, int] = field(default_factory=dict)
    use_channels: Optional[List[int]] = None
    area_index_by_ch: Optional[Dict[int, int]] = None
    cluster_mode: str = "distance"
    merge_distance_px: float = 80.0
    num_clusters: Optional[int] = None
    auto_k_min: int = 2
    auto_k_max: int = 8
    raw_point_radius: int = 5
    cluster_center_radius: int = 12
    text_scale: float = 0.5
    text_thickness: int = 1


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_path(path_str, base=None):
    if path_str is None:
        return None

    path_str = str(path_str).strip()

    if path_str == "":
        return None

    p = Path(path_str)

    if p.is_absolute():
        return p

    if base is not None:
        p2 = Path(base) / p

        if p2.exists():
            return p2.resolve()

    p3 = Path.cwd() / p

    if p3.exists():
        return p3.resolve()

    return p


def compute_homography(src_pts, dst_pts):
    src = np.asarray(src_pts, dtype=np.float32)
    dst = np.asarray(dst_pts, dtype=np.float32)

    if len(src) < 4 or len(dst) < 4 or len(src) != len(dst):
        return None

    H, _ = cv2.findHomography(src, dst, method=0)
    return H


def transform_point(H, x, y):
    pt = np.array([[[float(x), float(y)]]], dtype=np.float32)
    out = cv2.perspectiveTransform(pt, H)[0, 0]
    return float(out[0]), float(out[1])


def get_color(idx):
    hue = int((idx * 47) % 180)
    hsv = np.uint8([[[hue, 220, 255]]])
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0]
    return int(bgr[0]), int(bgr[1]), int(bgr[2])


def box_center_from_list(box):
    x1, y1, x2, y2 = map(float, box)
    return (x1 + x2) / 2.0, (y1 + y2) / 2.0


def euclidean_dist(p1, p2):
    return math.sqrt(
        (float(p1[0]) - float(p2[0])) ** 2
        + (float(p1[1]) - float(p2[1])) ** 2
    )


class TopViewPersonPositionManager:
    def __init__(self, config):
        self.config = config
        self.topview = None
        self.topview_path = None
        self.homography_by_ch = {}
        self.area_idx_by_ch = {}
        self.load_mapping()

    def load_mapping(self):
        json_path = resolve_path(self.config.annotation_json_path)

        if json_path is None or not json_path.exists():
            raise RuntimeError(f"annotation json not found: {self.config.annotation_json_path}")

        data = load_json(json_path)
        json_dir = json_path.parent

        topview_path = resolve_path(data.get("topview_image_path", ""), base=json_dir)

        if topview_path is not None and topview_path.exists():
            self.topview = cv2.imread(str(topview_path), cv2.IMREAD_COLOR)
            self.topview_path = str(topview_path)

        images_info = data.get("images", [])
        areas_data = data.get("areas", {})

        use_channels = self.config.use_channels

        for info in images_info:
            image_idx = int(info["image_idx"])
            ch = int(info["ch"])

            if use_channels is not None and ch not in use_channels:
                continue

            area_list = areas_data.get(str(image_idx), [])
            valid_areas = []

            for area_idx, area in enumerate(area_list):
                if not bool(area.get("enabled", True)):
                    continue

                src = area.get("src", [])
                dst = area.get("dst", [])

                H = compute_homography(src, dst)

                if H is None:
                    continue

                valid_areas.append({
                    "area_idx": int(area_idx),
                    "H": H,
                })

            if len(valid_areas) == 0:
                continue

            selected = valid_areas[0]

            if self.config.area_index_by_ch is not None and ch in self.config.area_index_by_ch:
                target_area_idx = int(self.config.area_index_by_ch[ch])

                for area in valid_areas:
                    if int(area["area_idx"]) == target_area_idx:
                        selected = area
                        break

            self.homography_by_ch[ch] = selected["H"]
            self.area_idx_by_ch[ch] = int(selected["area_idx"])

    def cam_id_to_ch(self, cam_id):
        cam_id = int(cam_id)

        if cam_id in self.config.cam_id_to_ch:
            return int(self.config.cam_id_to_ch[cam_id])

        return cam_id

    def project_yolo_results(self, yolo_result_lst):
        rows = []

        top_h = None
        top_w = None

        if self.topview is not None:
            top_h, top_w = self.topview.shape[:2]

        for yolo_result in yolo_result_lst:
            if yolo_result is None:
                continue

            cam_id = int(yolo_result.get("cam_id", -1))
            frame_idx = int(yolo_result.get("frame_idx", -1))
            ch = self.cam_id_to_ch(cam_id)

            if ch not in self.homography_by_ch:
                continue

            H = self.homography_by_ch[ch]
            area_idx = self.area_idx_by_ch.get(ch, -1)
            tracks = yolo_result.get("tracks", [])

            for track in tracks:
                track_id = int(track.get("track_id", -1))
                box = track.get("box", None)

                if box is None:
                    continue

                cx, cy = box_center_from_list(box)
                tx, ty = transform_point(H, cx, cy)

                in_topview = True

                if top_w is not None and top_h is not None:
                    in_topview = 0 <= tx < top_w and 0 <= ty < top_h

                rows.append({
                    "cam_id": cam_id,
                    "ch": ch,
                    "frame_idx": frame_idx,
                    "track_id": track_id,
                    "conf": float(track.get("conf", 0.0)),
                    "box": [float(v) for v in box],
                    "center_x": float(cx),
                    "center_y": float(cy),
                    "top_x": float(tx),
                    "top_y": float(ty),
                    "in_topview": bool(in_topview),
                    "selected_area_idx": int(area_idx),
                })

        return rows

    def cluster_distance(self, rows):
        valid_rows = [r for r in rows if bool(r["in_topview"])]

        clusters = []

        ordered = sorted(
            valid_rows,
            key=lambda r: float(r.get("conf", 0.0)),
            reverse=True,
        )

        for row in ordered:
            px = float(row["top_x"])
            py = float(row["top_y"])

            best_idx = -1
            best_dist = 999999.0

            for idx, cluster in enumerate(clusters):
                dist = euclidean_dist(
                    (px, py),
                    (cluster["mean_x"], cluster["mean_y"]),
                )

                if dist < best_dist:
                    best_dist = dist
                    best_idx = idx

            if best_idx >= 0 and best_dist <= self.config.merge_distance_px:
                cluster = clusters[best_idx]
                cluster["members"].append(row)

                xs = [float(m["top_x"]) for m in cluster["members"]]
                ys = [float(m["top_y"]) for m in cluster["members"]]

                cluster["mean_x"] = float(np.mean(xs))
                cluster["mean_y"] = float(np.mean(ys))
            else:
                clusters.append({
                    "mean_x": px,
                    "mean_y": py,
                    "members": [row],
                })

        return self.clusters_to_person_rows(clusters)

    def choose_best_k(self, points_xy):
        n = len(points_xy)

        if n <= 2:
            return 1

        k_min = max(2, int(self.config.auto_k_min))
        k_max = min(int(self.config.auto_k_max), n - 1)

        if k_min > k_max:
            return 1

        best_k = 1
        best_score = -1.0

        for k in range(k_min, k_max + 1):
            try:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(points_xy)

                if len(set(labels.tolist())) < 2:
                    continue

                score = silhouette_score(points_xy, labels)

                if score > best_score:
                    best_score = score
                    best_k = k
            except Exception:
                continue

        return int(best_k)

    def cluster_kmeans(self, rows):
        valid_rows = [r for r in rows if bool(r["in_topview"])]

        if len(valid_rows) == 0:
            return []

        if len(valid_rows) == 1:
            clusters = [{
                "mean_x": float(valid_rows[0]["top_x"]),
                "mean_y": float(valid_rows[0]["top_y"]),
                "members": [valid_rows[0]],
            }]

            return self.clusters_to_person_rows(clusters)

        points_xy = np.array(
            [[float(r["top_x"]), float(r["top_y"])] for r in valid_rows],
            dtype=np.float32,
        )

        if self.config.num_clusters is not None:
            k = int(self.config.num_clusters)
            k = max(1, min(k, len(valid_rows)))
        else:
            k = self.choose_best_k(points_xy)

        if k <= 1:
            labels = np.zeros((len(valid_rows),), dtype=np.int32)
        else:
            if not SKLEARN_AVAILABLE:
                return self.cluster_distance(rows)

            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(points_xy)

        clusters = []

        for cid in sorted(set(labels.tolist())):
            idxs = np.where(labels == cid)[0]
            members = [valid_rows[int(i)] for i in idxs.tolist()]
            xs = [float(m["top_x"]) for m in members]
            ys = [float(m["top_y"]) for m in members]

            clusters.append({
                "mean_x": float(np.mean(xs)),
                "mean_y": float(np.mean(ys)),
                "members": members,
            })

        return self.clusters_to_person_rows(clusters)

    def clusters_to_person_rows(self, clusters):
        person_rows = []

        clusters = sorted(
            clusters,
            key=lambda c: (float(c["mean_y"]), float(c["mean_x"])),
        )

        for person_id, cluster in enumerate(clusters):
            members = cluster["members"]

            member_rows = []

            for m in members:
                member_rows.append({
                    "cam_id": int(m["cam_id"]),
                    "ch": int(m["ch"]),
                    "track_id": int(m["track_id"]),
                    "conf": round(float(m["conf"]), 4),
                    "top_x": round(float(m["top_x"]), 2),
                    "top_y": round(float(m["top_y"]), 2),
                })

            person_rows.append({
                "person_id": int(person_id),
                "top_x": round(float(cluster["mean_x"]), 2),
                "top_y": round(float(cluster["mean_y"]), 2),
                "num_points": int(len(members)),
                "members": member_rows,
            })

        return person_rows

    def draw_topview(self, raw_rows, person_rows):
        if self.topview is None:
            return None

        out = self.topview.copy()

        for row in raw_rows:
            if not bool(row["in_topview"]):
                continue

            tx = int(round(float(row["top_x"])))
            ty = int(round(float(row["top_y"])))
            ch = int(row["ch"])
            track_id = int(row["track_id"])
            color = get_color(ch * 100 + track_id)

            cv2.circle(
                out,
                (tx, ty),
                self.config.raw_point_radius,
                color,
                -1,
                cv2.LINE_AA,
            )

            cv2.circle(
                out,
                (tx, ty),
                self.config.raw_point_radius + 2,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

            cv2.putText(
                out,
                f"CH{ch}_T{track_id}",
                (tx + 6, ty - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                self.config.text_scale,
                color,
                self.config.text_thickness,
                cv2.LINE_AA,
            )

        for person in person_rows:
            pid = int(person["person_id"])
            tx = int(round(float(person["top_x"])))
            ty = int(round(float(person["top_y"])))
            color = get_color(pid + 10)

            cv2.circle(
                out,
                (tx, ty),
                self.config.cluster_center_radius,
                color,
                -1,
                cv2.LINE_AA,
            )

            cv2.circle(
                out,
                (tx, ty),
                self.config.cluster_center_radius + 3,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )

            cv2.putText(
                out,
                f"PERSON_{pid} ({tx},{ty}) n={person['num_points']}",
                (tx + 12, ty - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                color,
                2,
                cv2.LINE_AA,
            )

        return out

    def process(self, yolo_result_lst, debug=False):
        raw_rows = self.project_yolo_results(yolo_result_lst)

        if self.config.cluster_mode.lower() == "kmeans":
            person_rows = self.cluster_kmeans(raw_rows)
        else:
            person_rows = self.cluster_distance(raw_rows)

        output_frame = None

        if debug:
            output_frame = self.draw_topview(raw_rows, person_rows)

        result = {
            "raw_points": raw_rows,
            "persons": person_rows,
            "count": {
                "raw_points": len(raw_rows),
                "valid_points": sum(1 for r in raw_rows if bool(r["in_topview"])),
                "persons": len(person_rows),
            },
        }

        return result, output_frame


def create_topview_manager(config):
    return TopViewPersonPositionManager(config=config)


def get_topview_person_positions(manager, yolo_result_lst, debug=False):
    return manager.process(
        yolo_result_lst=yolo_result_lst,
        debug=debug,
    )