from earth_base.config import *
import cv2
import numpy as np
import time
import queue


def video_playback():
    print("[INFO] Waiting for first frame...")

    while True:

        while frame_queue.empty():
            time.sleep(0.1)
        print("[INFO] First frame received, starting playback")

        time.sleep(10)  # Allow some time for the first frame to be processed

        cv2.namedWindow("Video Playback", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Video Playback", 1280, 720)

        while True:
            try:
                timestamp, frame_data = frame_queue.get(timeout=1)

                np_arr = np.frombuffer(frame_data, dtype=np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                if frame is None:
                    continue

                cv2.imshow("Video Playback", frame)

                wait_time = max(1, int(1000 / FRAME_RATE))
                if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                    break
            except queue.Empty:
                continue
            except Exception as e:
                print("[ERROR]", e)

        cv2.destroyAllWindows()
