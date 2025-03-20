import struct
import cv2
import numpy as np
from src.config import *


def receive_video_from_rover(recv_socket):
    print(f"[EARTH - RECEIVE] Listening for video on port {VIDEO_PORT}")
    while True:
        try:
            # Receive the full packet (use a sufficiently large buffer)
            packet, addr = recv_socket.recvfrom(65536)  # 64KB buffer
            if len(packet) < 4:
                print("[ERROR] Incomplete packet received.")
                continue

            # Extract header and frame data
            (frame_size,) = struct.unpack("!I", packet[:4])
            frame_data = packet[4:]

            print(f"[DEBUG] Received frame from {addr} of size: {frame_size}")

            if len(frame_data) != frame_size:
                print("[WARNING] Incomplete frame received.")
                continue

            np_frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
            if frame is None:
                print("[ERROR] Failed to decode frame.")
                continue

            cv2.imshow("Video from Rover", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        except Exception as e:
            print(f"[ERROR] Exception in receiving video: {e}")
