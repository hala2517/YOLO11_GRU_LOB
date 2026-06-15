import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
    "rtsp_transport;tcp|"
    "fflags;nobuffer|"
    "flags;low_delay|"
    "stimeout;5000000|"
    "rw_timeout;5000000|"
    "max_delay;500000"
)

import threading
import time
import cv2
from ultralytics import YOLO

from YOLO_lib import (
    YOLOTrackConfig,
    create_yolo_tracker,
    track_one_cctv_frame,
    make_blank_frame,
    make_8ch_grid,
)

from TopView_lib import (
    TopViewConfig,
    create_topview_manager,
    get_topview_person_positions,
)

from Action_Recognition_lib import (
    ActionRecognitionConfig,
    create_action_recognizer,
    recognize_action,
)

from Action_Classification_lib import (
    ActionClassificationConfig,
    create_action_classifier,
    classify_action_products,
)

from CycleTime_Balance_lib import (
    CycleTimeBalanceConfig,
    create_cycle_time_balance_manager,
    update_cycle_time_balance,
)


DEBUG = False

YOLO_DEBUG = True
TOPVIEW_DEBUG = True
ACTION_DEBUG = True
CLASSIFICATION_DEBUG = True
CYCLE_DEBUG = True

MODEL_PATH = r"./best.pt"

PRODUCT_CLASSIFIER_MODEL_PATH = r"./product_resnet18.pt"

PRODUCT_CLASS_NAMES = [
    "class_0",
    "class_1",
    "class_2",
]

CCTV_IP = [
    "100.120.1.20",
    "100.120.1.21",
    "100.120.1.22",
    "100.120.1.23",
    "100.120.1.24",
    "100.120.1.25",
    "100.120.1.26",
    "100.120.1.27",
]

CCTV_PW = [
    "admin1357!",
    "admin1357!",
    "admin1357!",
    "admin1357!",
    "admin1357!",
    "admin1357!",
    "admin1357!",
    "admin1357!",
]

CCTV_Agent = []


class CCTV_Thread(threading.Thread):
    def __init__(self, IP, PW):
        super().__init__()

        self.stop_event = threading.Event()
        self.lock = threading.Lock()

        self.IP = IP
        self.PW = PW

        self.latest_frame = None

        self.rtsp_url = "rtsp://admin:{0}@{1}:554/Streaming/Channels/101".format(PW, IP)

        self.cap = cv2.VideoCapture(self.rtsp_url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
        self.cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)

    def run(self):
        try:
            while not self.stop_event.is_set():
                if self.cap is None or not self.cap.isOpened():
                    time.sleep(0.2)
                    continue

                ret, frame = self.cap.read()

                if not ret or frame is None:
                    time.sleep(0.01)
                    continue

                with self.lock:
                    self.latest_frame = frame.copy()

                if DEBUG:
                    cv2.imshow(f"CCTV {self.IP}", frame)

                    key = cv2.waitKey(1) & 0xFF

                    if key == 27 or key == ord("q"):
                        break

        finally:
            print(f"[{self.IP}] Thread stopped.")

            if self.cap is not None:
                self.cap.release()

            if DEBUG:
                cv2.destroyAllWindows()

    def get_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None

            return self.latest_frame.copy()

    def stop(self):
        self.stop_event.set()


def start_cctv_threads():
    for ip, pw in zip(CCTV_IP, CCTV_PW):
        cctv = CCTV_Thread(IP=ip, PW=pw)
        cctv.start()
        CCTV_Agent.append(cctv)


def stop_cctv_threads():
    for cctv in CCTV_Agent:
        cctv.stop()

    for cctv in CCTV_Agent:
        cctv.join()


def get_frame_from_CCTV():
    frame_lst = []

    for cctv in CCTV_Agent:
        frame = cctv.get_frame()
        frame_lst.append(frame)

    return frame_lst


def calc_box_area_from_track(track):
    box = track.get("box", None)

    if box is None:
        return 0.0

    x1, y1, x2, y2 = map(float, box)

    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def find_track_from_yolo_results(yolo_result_lst, cam_id, track_id):
    cam_id = int(cam_id)
    track_id = int(track_id)

    for yolo_result in yolo_result_lst:
        if yolo_result is None:
            continue

        if int(yolo_result.get("cam_id", -1)) != cam_id:
            continue

        for track in yolo_result.get("tracks", []):
            if int(track.get("track_id", -1)) == track_id:
                return track

    return None


def make_action_input_from_topview(yolo_result_lst, topview_result):
    selected_by_cam = {}
    selected_person_rows = []

    persons = topview_result.get("persons", [])

    for person in persons:
        topview_person_id = int(person.get("person_id", -1))
        members = person.get("members", [])

        best_member = None
        best_track = None
        best_area = -1.0

        for member in members:
            cam_id = int(member.get("cam_id", -1))
            track_id = int(member.get("track_id", -1))

            track = find_track_from_yolo_results(
                yolo_result_lst=yolo_result_lst,
                cam_id=cam_id,
                track_id=track_id,
            )

            if track is None:
                continue

            area = calc_box_area_from_track(track)

            if area > best_area:
                best_area = area
                best_member = member
                best_track = track

        if best_track is None or best_member is None:
            continue

        selected_cam_id = int(best_member["cam_id"])
        selected_track_id = int(best_member["track_id"])

        copied_track = dict(best_track)
        copied_track["topview_person_id"] = topview_person_id
        copied_track["topview_x"] = float(person.get("top_x", 0.0))
        copied_track["topview_y"] = float(person.get("top_y", 0.0))
        copied_track["selected_bbox_area"] = float(best_area)

        if selected_cam_id not in selected_by_cam:
            selected_by_cam[selected_cam_id] = []

        selected_by_cam[selected_cam_id].append(copied_track)

        selected_person_rows.append({
            "topview_person_id": topview_person_id,
            "selected_cam_id": selected_cam_id,
            "selected_track_id": selected_track_id,
            "selected_bbox_area": float(best_area),
            "topview_x": float(person.get("top_x", 0.0)),
            "topview_y": float(person.get("top_y", 0.0)),
            "num_points": int(person.get("num_points", 0)),
            "members": members,
        })

    action_yolo_result_lst = []

    for yolo_result in yolo_result_lst:
        if yolo_result is None:
            continue

        cam_id = int(yolo_result.get("cam_id", -1))
        selected_tracks = selected_by_cam.get(cam_id, [])

        filtered_result = {
            "cam_id": cam_id,
            "frame_idx": int(yolo_result.get("frame_idx", 0)),
            "detections": yolo_result.get("detections", {}),
            "tracks": selected_tracks,
            "count": {
                "selected_person_tracks": len(selected_tracks),
            },
        }

        action_yolo_result_lst.append(filtered_result)

    return action_yolo_result_lst, selected_person_rows


def find_action_yolo_result_by_cam(action_yolo_result_lst, cam_id):
    cam_id = int(cam_id)

    for item in action_yolo_result_lst:
        if item is None:
            continue

        if int(item.get("cam_id", -1)) == cam_id:
            return item

    return None


def draw_selected_person_info(frame_lst, selected_person_rows):
    for row in selected_person_rows:
        cam_id = int(row["selected_cam_id"])

        if cam_id < 0 or cam_id >= len(frame_lst):
            continue

        frame = frame_lst[cam_id]

        if frame is None:
            continue

        text = (
            f"TOP_PERSON {row['topview_person_id']} "
            f"AREA {row['selected_bbox_area']:.0f}"
        )

        cv2.putText(
            frame,
            text,
            (20, 70 + 30 * int(row["topview_person_id"])),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )


def print_topview_result(topview_result, selected_person_rows):
    print("[TOPVIEW]", topview_result.get("count", {}))

    for row in selected_person_rows:
        print(
            f"[SELECTED] "
            f"person={row['topview_person_id']} "
            f"top=({row['topview_x']:.1f}, {row['topview_y']:.1f}) "
            f"cam={row['selected_cam_id']} "
            f"track={row['selected_track_id']} "
            f"area={row['selected_bbox_area']:.1f} "
            f"points={row['num_points']}"
        )


def print_action_result(action_result_lst):
    for action_result in action_result_lst:
        if action_result is None:
            continue

        cam_id = action_result.get("cam_id", -1)
        frame_idx = action_result.get("frame_idx", -1)
        count_info = action_result.get("count", {})

        print(
            f"[ACTION] "
            f"cam={cam_id} "
            f"frame={frame_idx} "
            f"person={count_info.get('person', 0)} "
            f"work={count_info.get('work', 0)} "
            f"pick={count_info.get('pick', 0)} "
            f"place={count_info.get('place', 0)}"
        )


def print_classification_result(classification_result_lst):
    for classification_result in classification_result_lst:
        if classification_result is None:
            continue

        cam_id = classification_result.get("cam_id", -1)
        frame_idx = classification_result.get("frame_idx", -1)

        for item in classification_result.get("classifications", []):
            print(
                f"[CLASSIFY] "
                f"cam={cam_id} "
                f"frame={frame_idx} "
                f"top_person={item.get('topview_person_id', -1)} "
                f"track={item.get('track_id', -1)} "
                f"action={item.get('action', '')} "
                f"class={item.get('class_name', '')} "
                f"prob={float(item.get('prob', 0.0)):.3f}"
            )


def print_cycle_result(cycle_result):
    for event in cycle_result.get("cycle_events", []):
        print(
            f"[CYCLE] "
            f"person={event['stable_person_id']} "
            f"ct={event['cycle_time_sec']:.2f}s "
            f"product={event.get('product_class_name', '')}"
        )

    for person in cycle_result.get("persons", []):
        if person.get("avg_cycle_time_sec", None) is None:
            continue

        print(
            f"[LOB/EB] "
            f"person={person['stable_person_id']} "
            f"count={person['cycle_count']} "
            f"avg_ct={person['avg_cycle_time_sec']}s "
            f"lob={person['lob_percent']}% "
            f"eb={person['eb_percent']}%"
        )

    print("[LINE EB]", cycle_result.get("line", {}))


def get_frame_key_from_yolo_results(yolo_result_lst):
    frame_key = 0

    for yolo_result in yolo_result_lst:
        if yolo_result is None:
            continue

        frame_idx = int(yolo_result.get("frame_idx", 0))
        frame_key = max(frame_key, frame_idx)

    return frame_key


def main():
    start_cctv_threads()

    model = YOLO(MODEL_PATH)

    yolo_config = YOLOTrackConfig(
        device=0,
        imgsz=640,
        conf=0.20,
        iou=0.45,
        max_det=2000,
        person_class_ids=(0,),
        hand_class_ids=(1,),
        hat_class_ids=(2,),
        product_class_ids=(3,),
    )

    yolo_manager = create_yolo_tracker(
        model=model,
        num_cctv=len(CCTV_IP),
        config=yolo_config,
    )

    topview_config = TopViewConfig(
        annotation_json_path=r"./manual_multi_area_topview_overlap_out/multi_area_6pt_annotations.json",
        cam_id_to_ch={
            0: 2,
            1: 3,
            2: 5,
            3: 6,
        },
        use_channels=[2, 3, 5, 6],
        area_index_by_ch={
            2: 0,
            3: 0,
            5: 0,
            6: 0,
        },
        cluster_mode="distance",
        merge_distance_px=80.0,
    )

    topview_manager = create_topview_manager(
        config=topview_config,
    )

    action_config = ActionRecognitionConfig(
        close_dist_norm=0.45,
        pick_confirm_frames=3,
        place_confirm_frames=5,
        min_hold_frames=8,
        event_display_frames=15,
        max_missing_frames=30,
    )

    action_manager = create_action_recognizer(
        num_cctv=len(CCTV_IP),
        config=action_config,
    )

    classification_config = ActionClassificationConfig(
        image_size=224,
        crop_margin=0.15,
        topk=3,
        classify_only_holding=True,
        classify_actions=("Pick", "Work"),
        device=None,
    )

    classification_manager = create_action_classifier(
        model_path=PRODUCT_CLASSIFIER_MODEL_PATH,
        class_names=PRODUCT_CLASS_NAMES,
        config=classification_config,
    )

    cycle_config = CycleTimeBalanceConfig(
        cycle_event_names=("Place",),
        cycle_window_size=20,
        min_cycle_time_sec=0.5,
        max_cycle_time_sec=300.0,
        min_event_gap_sec=0.5,
        topview_match_distance_px=120.0,
        stable_person_lost_sec=5.0,
        target_cycle_time_sec=None,
    )

    cycle_manager = create_cycle_time_balance_manager(
        config=cycle_config,
    )

    try:
        while True:
            frame_lst = get_frame_from_CCTV()

            yolo_result_lst = []
            display_frame_lst = []

            for cam_id, frame in enumerate(frame_lst):
                if frame is None:
                    yolo_result_lst.append(None)
                    display_frame_lst.append(
                        make_blank_frame(
                            width=640,
                            height=480,
                            text=f"CCTV {cam_id} frame none",
                        )
                    )
                    continue

                yolo_result, yolo_output_frame = track_one_cctv_frame(
                    manager=yolo_manager,
                    frame=frame,
                    cam_id=cam_id,
                    debug=YOLO_DEBUG,
                )

                yolo_result_lst.append(yolo_result)

                if YOLO_DEBUG and yolo_output_frame is not None:
                    display_frame_lst.append(yolo_output_frame)
                else:
                    display_frame_lst.append(frame.copy())

            topview_result, topview_output_frame = get_topview_person_positions(
                manager=topview_manager,
                yolo_result_lst=yolo_result_lst,
                debug=TOPVIEW_DEBUG,
            )

            action_yolo_result_lst, selected_person_rows = make_action_input_from_topview(
                yolo_result_lst=yolo_result_lst,
                topview_result=topview_result,
            )

            action_result_lst = []
            classification_result_lst = []

            for action_yolo_result in action_yolo_result_lst:
                cam_id = int(action_yolo_result.get("cam_id", -1))

                if cam_id < 0 or cam_id >= len(frame_lst):
                    continue

                original_frame = frame_lst[cam_id]

                if original_frame is None:
                    continue

                base_frame = display_frame_lst[cam_id]

                action_result, action_output_frame = recognize_action(
                    manager=action_manager,
                    yolo_result=action_yolo_result,
                    frame=base_frame,
                    cam_id=cam_id,
                    debug=ACTION_DEBUG,
                )

                action_result_lst.append(action_result)

                if ACTION_DEBUG and action_output_frame is not None:
                    display_frame_lst[cam_id] = action_output_frame

                classification_result, classification_output_frame = classify_action_products(
                    manager=classification_manager,
                    frame=original_frame,
                    action_result=action_result,
                    action_yolo_result=action_yolo_result,
                    debug=CLASSIFICATION_DEBUG,
                    draw_frame=display_frame_lst[cam_id],
                )

                classification_result_lst.append(classification_result)

                if CLASSIFICATION_DEBUG and classification_output_frame is not None:
                    display_frame_lst[cam_id] = classification_output_frame

            frame_key = get_frame_key_from_yolo_results(yolo_result_lst)

            cycle_result, cycle_output_frame = update_cycle_time_balance(
                manager=cycle_manager,
                action_result_lst=action_result_lst,
                selected_person_rows=selected_person_rows,
                classification_result_lst=classification_result_lst,
                timestamp_sec=time.time(),
                frame_key=frame_key,
                debug=CYCLE_DEBUG,
            )

            draw_selected_person_info(
                frame_lst=display_frame_lst,
                selected_person_rows=selected_person_rows,
            )

            if YOLO_DEBUG or ACTION_DEBUG or CLASSIFICATION_DEBUG:
                grid = make_8ch_grid(
                    frames=display_frame_lst,
                    view_w=640,
                    view_h=360,
                )

                cv2.imshow("8 CCTV Detection + Action + Classification", grid)

            if TOPVIEW_DEBUG and topview_output_frame is not None:
                cv2.imshow("TopView Person Integration", topview_output_frame)

            if CYCLE_DEBUG and cycle_output_frame is not None:
                cv2.imshow("Cycle Time / LOB / EB", cycle_output_frame)

            print_topview_result(
                topview_result=topview_result,
                selected_person_rows=selected_person_rows,
            )

            print_action_result(
                action_result_lst=action_result_lst,
            )

            print_classification_result(
                classification_result_lst=classification_result_lst,
            )

            print_cycle_result(
                cycle_result=cycle_result,
            )

            key = cv2.waitKey(1) & 0xFF

            if key == 27 or key == ord("q"):
                break

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[Main] Stop requested.")

    finally:
        stop_cctv_threads()
        cv2.destroyAllWindows()
        print("[Main] finished.")


if __name__ == "__main__":
    main()