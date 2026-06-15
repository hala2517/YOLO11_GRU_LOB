import time
import cv2
import math
import numpy as np
from dataclasses import dataclass, field
from collections import deque
from typing import Dict, List, Any, Optional, Tuple


@dataclass
class CycleTimeBalanceConfig:
    cycle_event_names: Tuple[str, ...] = ("Place",)
    cycle_action_names: Tuple[str, ...] = ()
    cycle_window_size: int = 20
    min_cycle_time_sec: float = 0.5
    max_cycle_time_sec: float = 300.0
    min_event_gap_sec: float = 0.5
    topview_match_distance_px: float = 120.0
    stable_person_lost_sec: float = 5.0
    target_cycle_time_sec: Optional[float] = None
    draw_width: int = 1000
    draw_height: int = 520


@dataclass
class StableTopViewPerson:
    stable_id: int
    top_x: float
    top_y: float
    last_seen_time: float
    last_seen_frame_key: int = 0


@dataclass
class PersonCycleState:
    stable_id: int
    cycle_times: deque = field(default_factory=deque)
    last_cycle_event_time: Optional[float] = None
    last_cycle_event_frame_key: Optional[int] = None
    last_event_name: str = ""
    last_product_class: str = ""
    last_product_prob: float = 0.0
    total_cycle_count: int = 0

    def append_cycle_time(self, cycle_time_sec, config):
        if self.cycle_times.maxlen != config.cycle_window_size:
            old_values = list(self.cycle_times)
            self.cycle_times = deque(old_values[-config.cycle_window_size:], maxlen=config.cycle_window_size)

        self.cycle_times.append(float(cycle_time_sec))
        self.total_cycle_count += 1


def now_sec():
    return float(time.time())


def dist_xy(a, b):
    return math.sqrt(
        (float(a[0]) - float(b[0])) ** 2
        + (float(a[1]) - float(b[1])) ** 2
    )


def mean_safe(values):
    values = list(values)

    if len(values) == 0:
        return None

    return float(np.mean(values))


def std_safe(values):
    values = list(values)

    if len(values) == 0:
        return None

    return float(np.std(values))


def build_classification_map(classification_result_lst):
    result = {}

    if classification_result_lst is None:
        return result

    for class_result in classification_result_lst:
        if class_result is None:
            continue

        cam_id = int(class_result.get("cam_id", -1))

        for item in class_result.get("classifications", []):
            track_id = int(item.get("track_id", -1))

            if cam_id < 0 or track_id < 0:
                continue

            result[(cam_id, track_id)] = item

    return result


class CycleTimeBalanceManager:
    def __init__(self, config=None):
        self.config = config if config is not None else CycleTimeBalanceConfig()
        self.next_stable_person_id = 1
        self.stable_persons: Dict[int, StableTopViewPerson] = {}
        self.cycle_states: Dict[int, PersonCycleState] = {}

    def reset(self):
        self.next_stable_person_id = 1
        self.stable_persons = {}
        self.cycle_states = {}

    def get_cycle_state(self, stable_id):
        stable_id = int(stable_id)

        if stable_id not in self.cycle_states:
            self.cycle_states[stable_id] = PersonCycleState(
                stable_id=stable_id,
                cycle_times=deque(maxlen=self.config.cycle_window_size),
            )

        return self.cycle_states[stable_id]

    def remove_lost_stable_persons(self, t):
        delete_ids = []

        for stable_id, person in self.stable_persons.items():
            if float(t) - float(person.last_seen_time) > self.config.stable_person_lost_sec:
                delete_ids.append(stable_id)

        for stable_id in delete_ids:
            del self.stable_persons[stable_id]

    def assign_stable_person_ids(self, selected_person_rows, t, frame_key):
        used_stable_ids = set()
        rows_out = []

        sorted_rows = sorted(
            selected_person_rows,
            key=lambda r: float(r.get("selected_bbox_area", 0.0)),
            reverse=True,
        )

        for row in sorted_rows:
            top_x = float(row.get("topview_x", 0.0))
            top_y = float(row.get("topview_y", 0.0))

            best_id = None
            best_dist = 999999.0

            for stable_id, person in self.stable_persons.items():
                if stable_id in used_stable_ids:
                    continue

                d = dist_xy(
                    (top_x, top_y),
                    (person.top_x, person.top_y),
                )

                if d < best_dist:
                    best_dist = d
                    best_id = stable_id

            if best_id is not None and best_dist <= self.config.topview_match_distance_px:
                stable_id = int(best_id)
                self.stable_persons[stable_id].top_x = top_x
                self.stable_persons[stable_id].top_y = top_y
                self.stable_persons[stable_id].last_seen_time = float(t)
                self.stable_persons[stable_id].last_seen_frame_key = int(frame_key)
            else:
                stable_id = int(self.next_stable_person_id)
                self.next_stable_person_id += 1

                self.stable_persons[stable_id] = StableTopViewPerson(
                    stable_id=stable_id,
                    top_x=top_x,
                    top_y=top_y,
                    last_seen_time=float(t),
                    last_seen_frame_key=int(frame_key),
                )

            used_stable_ids.add(stable_id)

            new_row = dict(row)
            new_row["stable_person_id"] = stable_id
            rows_out.append(new_row)

        self.remove_lost_stable_persons(t)

        return rows_out

    def build_stable_id_map(self, selected_person_rows):
        out = {}

        for row in selected_person_rows:
            cam_id = int(row.get("selected_cam_id", -1))
            track_id = int(row.get("selected_track_id", -1))
            stable_id = int(row.get("stable_person_id", -1))

            if cam_id < 0 or track_id < 0 or stable_id < 0:
                continue

            out[(cam_id, track_id)] = stable_id

        return out

    def is_cycle_event(self, person):
        event = str(person.get("event", ""))
        action = str(person.get("action", ""))

        if event in self.config.cycle_event_names:
            return True, event

        if action in self.config.cycle_action_names:
            return True, action

        return False, ""

    def update_cycle_event(
        self,
        stable_id,
        event_name,
        t,
        frame_key,
        product_class_name="",
        product_prob=0.0,
    ):
        state = self.get_cycle_state(stable_id)

        if state.last_cycle_event_time is not None:
            gap = float(t) - float(state.last_cycle_event_time)

            if gap < self.config.min_event_gap_sec:
                return None

            if self.config.min_cycle_time_sec <= gap <= self.config.max_cycle_time_sec:
                state.append_cycle_time(gap, self.config)

                cycle_event = {
                    "stable_person_id": int(stable_id),
                    "cycle_time_sec": round(float(gap), 4),
                    "event": str(event_name),
                    "frame_key": int(frame_key),
                    "product_class_name": str(product_class_name),
                    "product_prob": round(float(product_prob), 4),
                    "cycle_count": int(state.total_cycle_count),
                }
            else:
                cycle_event = None
        else:
            cycle_event = None

        state.last_cycle_event_time = float(t)
        state.last_cycle_event_frame_key = int(frame_key)
        state.last_event_name = str(event_name)
        state.last_product_class = str(product_class_name)
        state.last_product_prob = float(product_prob)

        return cycle_event

    def compute_metrics(self):
        person_rows = []

        for stable_id, state in sorted(self.cycle_states.items(), key=lambda x: int(x[0])):
            avg_ct = mean_safe(state.cycle_times)
            std_ct = std_safe(state.cycle_times)

            if avg_ct is None:
                person_rows.append({
                    "stable_person_id": int(stable_id),
                    "cycle_count": int(state.total_cycle_count),
                    "window_count": int(len(state.cycle_times)),
                    "last_cycle_time_sec": None,
                    "avg_cycle_time_sec": None,
                    "std_cycle_time_sec": None,
                    "lob_percent": None,
                    "eb_percent": None,
                    "target_eff_percent": None,
                    "last_product_class": state.last_product_class,
                    "last_product_prob": round(float(state.last_product_prob), 4),
                })
                continue

            last_ct = float(state.cycle_times[-1]) if len(state.cycle_times) > 0 else None

            person_rows.append({
                "stable_person_id": int(stable_id),
                "cycle_count": int(state.total_cycle_count),
                "window_count": int(len(state.cycle_times)),
                "last_cycle_time_sec": round(float(last_ct), 4) if last_ct is not None else None,
                "avg_cycle_time_sec": round(float(avg_ct), 4),
                "std_cycle_time_sec": round(float(std_ct), 4) if std_ct is not None else None,
                "lob_percent": None,
                "eb_percent": None,
                "target_eff_percent": None,
                "last_product_class": state.last_product_class,
                "last_product_prob": round(float(state.last_product_prob), 4),
            })

        valid_avg = [
            float(row["avg_cycle_time_sec"])
            for row in person_rows
            if row["avg_cycle_time_sec"] is not None
        ]

        line_metrics = {
            "person_count": len(person_rows),
            "valid_person_count": len(valid_avg),
            "bottleneck_cycle_time_sec": None,
            "fastest_cycle_time_sec": None,
            "line_eb_percent": None,
            "target_cycle_time_sec": self.config.target_cycle_time_sec,
        }

        if len(valid_avg) == 0:
            return person_rows, line_metrics

        bottleneck_ct = max(valid_avg)
        fastest_ct = min(valid_avg)

        line_eb = None

        if bottleneck_ct > 0 and len(valid_avg) > 0:
            line_eb = sum(valid_avg) / (len(valid_avg) * bottleneck_ct) * 100.0

        for row in person_rows:
            avg_ct = row["avg_cycle_time_sec"]

            if avg_ct is None or avg_ct <= 0:
                continue

            row["lob_percent"] = round(float(avg_ct) / float(bottleneck_ct) * 100.0, 2)
            row["eb_percent"] = round(float(fastest_ct) / float(avg_ct) * 100.0, 2)

            if self.config.target_cycle_time_sec is not None and self.config.target_cycle_time_sec > 0:
                row["target_eff_percent"] = round(
                    float(self.config.target_cycle_time_sec) / float(avg_ct) * 100.0,
                    2,
                )

        line_metrics["bottleneck_cycle_time_sec"] = round(float(bottleneck_ct), 4)
        line_metrics["fastest_cycle_time_sec"] = round(float(fastest_ct), 4)
        line_metrics["line_eb_percent"] = round(float(line_eb), 2) if line_eb is not None else None

        return person_rows, line_metrics

    def process(
        self,
        action_result_lst,
        selected_person_rows,
        classification_result_lst=None,
        timestamp_sec=None,
        frame_key=None,
        debug=False,
    ):
        t = now_sec() if timestamp_sec is None else float(timestamp_sec)

        if frame_key is None:
            frame_key = int(t * 1000)

        selected_person_rows = self.assign_stable_person_ids(
            selected_person_rows=selected_person_rows,
            t=t,
            frame_key=frame_key,
        )

        stable_map = self.build_stable_id_map(selected_person_rows)
        classification_map = build_classification_map(classification_result_lst)

        cycle_events = []

        for action_result in action_result_lst:
            if action_result is None:
                continue

            cam_id = int(action_result.get("cam_id", -1))

            for person in action_result.get("persons", []):
                track_id = int(person.get("track_id", -1))

                if cam_id < 0 or track_id < 0:
                    continue

                key = (cam_id, track_id)

                if key not in stable_map:
                    continue

                is_event, event_name = self.is_cycle_event(person)

                if not is_event:
                    continue

                stable_id = int(stable_map[key])

                class_item = classification_map.get(key, {})
                product_class_name = str(class_item.get("class_name", ""))
                product_prob = float(class_item.get("prob", 0.0))

                cycle_event = self.update_cycle_event(
                    stable_id=stable_id,
                    event_name=event_name,
                    t=t,
                    frame_key=frame_key,
                    product_class_name=product_class_name,
                    product_prob=product_prob,
                )

                if cycle_event is not None:
                    cycle_events.append(cycle_event)

        person_metrics, line_metrics = self.compute_metrics()

        result = {
            "selected_persons": selected_person_rows,
            "cycle_events": cycle_events,
            "persons": person_metrics,
            "line": line_metrics,
        }

        output_frame = None

        if debug:
            output_frame = draw_cycle_balance_panel(
                result=result,
                width=self.config.draw_width,
                height=self.config.draw_height,
            )

        return result, output_frame


def draw_cycle_balance_panel(result, width=1000, height=520):
    panel = np.zeros((height, width, 3), dtype=np.uint8)
    panel[:] = (25, 25, 25)

    line = result.get("line", {})
    persons = result.get("persons", [])
    events = result.get("cycle_events", [])

    title = "Cycle Time / LOB / EB"

    cv2.putText(
        panel,
        title,
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    line_text = (
        f"Valid={line.get('valid_person_count', 0)} "
        f"Bottleneck={line.get('bottleneck_cycle_time_sec')}s "
        f"Fastest={line.get('fastest_cycle_time_sec')}s "
        f"LineEB={line.get('line_eb_percent')}%"
    )

    cv2.putText(
        panel,
        line_text,
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (200, 255, 200),
        2,
        cv2.LINE_AA,
    )

    header = "ID | Count | Last CT | Avg CT | LOB% | EB% | Product"
    cv2.putText(
        panel,
        header,
        (30, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (180, 180, 180),
        2,
        cv2.LINE_AA,
    )

    y = 160

    for row in persons[:10]:
        sid = row.get("stable_person_id")
        count = row.get("cycle_count")
        last_ct = row.get("last_cycle_time_sec")
        avg_ct = row.get("avg_cycle_time_sec")
        lob = row.get("lob_percent")
        eb = row.get("eb_percent")
        product = row.get("last_product_class", "")

        text = (
            f"{sid:>2} | "
            f"{count:>5} | "
            f"{str(last_ct):>7} | "
            f"{str(avg_ct):>6} | "
            f"{str(lob):>5} | "
            f"{str(eb):>5} | "
            f"{product}"
        )

        color = (255, 255, 255)

        if lob is not None and lob >= 95:
            color = (0, 180, 255)

        cv2.putText(
            panel,
            text,
            (30, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            color,
            2,
            cv2.LINE_AA,
        )

        y += 34

    if len(events) > 0:
        cv2.putText(
            panel,
            "Recent Cycle Events",
            (570, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (180, 180, 180),
            2,
            cv2.LINE_AA,
        )

        ey = 160

        for event in events[-8:]:
            text = (
                f"P{event['stable_person_id']} "
                f"CT={event['cycle_time_sec']}s "
                f"{event.get('product_class_name', '')}"
            )

            cv2.putText(
                panel,
                text,
                (570, ey),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

            ey += 32

    return panel


def create_cycle_time_balance_manager(config=None):
    return CycleTimeBalanceManager(config=config)


def update_cycle_time_balance(
    manager,
    action_result_lst,
    selected_person_rows,
    classification_result_lst=None,
    timestamp_sec=None,
    frame_key=None,
    debug=False,
):
    return manager.process(
        action_result_lst=action_result_lst,
        selected_person_rows=selected_person_rows,
        classification_result_lst=classification_result_lst,
        timestamp_sec=timestamp_sec,
        frame_key=frame_key,
        debug=debug,
    )