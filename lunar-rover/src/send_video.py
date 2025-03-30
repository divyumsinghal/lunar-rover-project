import time
import cv2
import os
from src.config import *
from utils.client_server_comm import secure_send


def send_video_to_earth(send_socket):
    while True:
        if not video_queue.empty():
            try:
                command = video_queue.get()
                if command != video_1:
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
                        ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70]
                    )
                    if not ret:
                        continue

                    frame_data = buffer.tobytes()
                    destination = (EARTH_BASE_IP, EARTH_RECIEVE_VIDEO_PORT)

                    try:
                        secure_send(
                            frames_sent,
                            send_socket,
                            frame_data,
                            destination,
                            packet_type=MSG_TYPE_VIDEO,
                        )
                        frames_sent += 1
                    except Exception:
                        continue

                    if frame_rate > 0:
                        time.sleep(1.0 / frame_rate)

                cap.release()
            except Exception:
                continue
        else:
            time.sleep(0.1)
