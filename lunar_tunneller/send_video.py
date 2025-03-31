import time
import cv2
import os
from lunar_tunneller.config import *
from utils.client_server_comm import secure_send
import threading
from multiprocessing import Process


def send_video_to_rover(send_socket):
    while True:
        if not video_queue.empty():
            try:
                command = video_queue.get()
                if command != video_2:
                    continue

                if not os.path.exists(VIDEO_PATH):
                    continue

                cap = cv2.VideoCapture(VIDEO_PATH)
                if not cap.isOpened():
                    continue

                frame_rate = cap.get(cv2.CAP_PROP_FPS)
                frames_sent = 0

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    ret, buffer = cv2.imencode(
                        ".jpeg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70]
                    )
                    if not ret:
                        continue

                    frame_data = buffer.tobytes()
                    address = (LUNAR_ROVER_1_IP, ROVER_RECIEVE_VIDEO_PORT)

                    try:

                        p = Process(
                            target=secure_send,
                            args=(
                                frames_sent,
                                send_socket,
                                frame_data,
                                address,
                                MSG_TYPE_VIDEO,
                                earth_moon,
                            ),
                        )
                        p.start()

                        frames_sent += 1

                        if frames_sent % 100 == 0:
                            print(
                                f"[ROVER - SEND] Sent frame {frames_sent} to LUNAR ROVER"
                            )

                    except Exception:
                        continue

                cap.release()
                p.join()

            except Exception:
                continue

        else:
            time.sleep(0.1)
