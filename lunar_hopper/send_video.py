import time
import cv2
import os
from lunar_hopper.config import *
from utils.client_server_comm import secure_send, secure_receive
from multiprocessing import Process
import lunar_hopper.config as config
import msgpack
import socket


def send_video_to_rover(send_socket):
    while True:
        while not config.connection_with_rover:
            # print("[send_data_to_rover - SEND] Waiting for connection with rover...")
            time.sleep(0.5)

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

                        video_to_send[frames_sent] = frame_data

                        p = Process(
                            target=secure_send,
                            args=(
                                frames_sent,
                                send_socket,
                                frame_data,
                                address,
                                MSG_TYPE_VIDEO,
                                moon_moon,
                                SECRET_KEY_INTERNAL,
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

                time.sleep(5)
                video_to_send.clear()

            except Exception:
                continue

        else:
            time.sleep(0.1)


def get_nack_for_video(recv_sock):
    while True:
        while not config.connection_with_rover:
            # print("[send_data_to_rover - SEND] Waiting for connection with rover...")
            time.sleep(0.5)

        p = None

        try:
            recv_sock.settimeout(wait_time)
            seq_num, data_bytes, addr = secure_receive(recv_sock)
            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = int(message.get(message_data))
                address = (LUNAR_ROVER_1_IP, ROVER_RECIEVE_VIDEO_PORT)

                if recieved_type == nak:

                    p = Process(
                        target=secure_send,
                        args=(
                            payload,
                            recv_sock,
                            video_to_send[payload],
                            address,
                            MSG_TYPE_VIDEO,
                            moon_moon,
                        ),
                    )
                    p.start()

        except socket.timeout:
            # print("[send_data_to_rover - SEND] Timeout while receiving data.")
            if p:
                p.join()

        except Exception as e:
            # print(f"[ERROR send_video_to_rover] Error: {e}")
            continue
