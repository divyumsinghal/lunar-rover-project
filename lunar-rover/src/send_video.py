import time
import cv2
import struct
from src.config import *


def send_video_to_earth(send_socket):
    print(
        f"[EARTH COMM - SEND] Sending video data to Earth on port {EARTH_RECIEVE_VIDEO_PORT}"
    )
    while True:
        if not video_queue.empty():
            try:
                command = video_queue.get()
                if command == video_1:
                    print(f"[EARTH - send_video_to_earth] Command received: {command}")
                    cap = cv2.VideoCapture(VIDEO_PATH)
                    if not cap.isOpened():
                        print("[ERROR] Could not open video file.")
                        continue

                    while cap.isOpened():

                        try:
                            ret, frame = cap.read()
                            if not ret:
                                print("[INFO] End of video stream.")
                                break

                            # Adjust JPEG quality to reduce frame size
                            ret2, buffer = cv2.imencode(
                                ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50]
                            )
                            if not ret2:
                                print("[WARNING] Failed to encode frame; skipping.")
                                continue

                            frame_data = buffer.tobytes()
                            size = len(frame_data)
                            print(f"[DEBUG] Sending frame of size: {size} bytes")

                            # Create a single packet: 4-byte header + frame data
                            packet = struct.pack("!I", size) + frame_data
                            send_socket.sendto(
                                packet, (EARTH_BASE_IP, EARTH_RECIEVE_VIDEO_PORT)
                            )
                            time.sleep(1 / 30)

                        except Exception as e:
                            print(
                                f"[ERROR send_video_to_earth] Exception in send_video_to_earth: {e}"
                            )

                    cap.release()
                else:
                    print(f"[ERROR send_video_to_earth] Invalid command: {command}")
            except Exception as e:
                print(f"[ERROR send_video_to_earth] Failed to send data: {e}")
