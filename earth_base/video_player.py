from earth_base.config import *
import earth_base.config as config
import cv2
import numpy as np
import time
import queue


def video_playback():
    print("[INFO] Waiting for first frame...")

    video_num = 0

    while True:

        while not config.connection_with_rover:
            time.sleep(0.1)

        try:

            while play_frame_queue.empty():
                time.sleep(0.1)
            print("[INFO] First frame received, starting playback")

            time.sleep(2)  # Allow some time for the buffering to be processed

            cv2.namedWindow("Video Playback", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Video Playback", 300, 300)

            grace_period = 0

            last_played_frame = 0

            while True:

                try:
                    timestamp, frame_data = play_frame_queue.get(timeout=1)

                    np_arr = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                    if frame is None:
                        continue

                    if timestamp > last_played_frame:
                        last_played_frame = timestamp
                        cv2.imshow("Video Playback", frame)

                        wait_time = max(1, int(1000 / FRAME_RATE))
                        if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                            break

                except queue.Empty:
                    grace_period += 1
                    if grace_period > 10:
                        print(
                            "[INFO] No frames received for 10 seconds, stopping playback."
                        )
                        config.asked_for_video = False
                        break

                    else:
                        time.sleep(1)
                        continue

                except Exception as e:
                    print("[ERROR]", e)

            grace_period = 0

            fps = FRAME_RATE

            frame_width = 144
            frame_height = 256

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_num += 1
            video_number = str(video_num)

            out = cv2.VideoWriter(
                f"output{video_number}.mp4",
                fourcc,
                fps,
                (frame_width, frame_height),
            )

            # Write frames to video in order
            for i in sorted(video_to_store.keys()):
                if video_to_store[i] is None:
                    continue

                np_arr = np.frombuffer(video_to_store[i], dtype=np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is None:
                    continue

                out.write(frame)

            out.release()
            video_to_store.clear()

            cv2.destroyAllWindows()

            print("[INFO] Video saved as output" + video_number + ".mp4")

        except Exception as e:
            print("[ERROR]", e)
