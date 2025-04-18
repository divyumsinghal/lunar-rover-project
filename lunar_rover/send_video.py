import time
import cv2
import os
from lunar_rover.config import *
import lunar_rover.config as config
from utils.client_server_comm import secure_send, secure_send_with_ack, secure_receive
import msgpack
import threading
from multiprocessing import Process
import random
import socket


def send_video_to_earth(send_socket):
    while True:

        while not config.connection_with_earth:
            time.sleep(0.1)

        if not video_queue.empty():
            try:

                command = video_queue.get()
                if command == video_1:

                    address = (EARTH_BASE_IP, EARTH_RECIEVE_VIDEO_PORT)

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
                                    earth_moon,
                                    SECRET_KEY_INTERNAL,
                                ),
                            )
                            p.start()

                            frames_sent += 1

                            # if frames_sent % 100 == 0:
                            #    print(
                            #        f"[ROVER - SEND] Sent frame {frames_sent} to Earth Base"
                            #    )

                        except Exception:
                            continue

                    cap.release()
                    p.join()

                    time.sleep(5)
                    video_to_send.clear()

                elif command == video_2:

                    print("processing video_2")

                    if not config.connection_with_tunneller:
                        print("video 2 unavailable")

                        threading.Thread(
                            target=secure_send_with_ack,
                            args=(
                                send_socket,
                                {
                                    message_type: sens,
                                    message_data: tunneller_unavailable,
                                },
                                (EARTH_BASE_IP, EARTH_SEND_DATA_PORT_1),
                                retries,
                                wait_time,
                                seq_num,
                                MSG_TYPE_COMMAND,
                                earth_moon,
                                SECRET_KEY_INTERNAL,
                            ),
                            daemon=True,
                        ).start()

                    else:

                        print("video 2 available")

                        send_data = {
                            message_type: video,
                        }

                        send_data.update({message_data: video_2})

                        config.asked_for_video = True
                        config.tunneller_video = True

                        send_socket.settimeout(wait_time)
                        seq_num = random.randint(1, 1000000)
                        address = (LUNAR_TUNNELLER_IP, LUNAR_TUNNELLER_RECV_CMD_PORT)

                        threading.Thread(
                            target=secure_send_with_ack,
                            args=(
                                send_socket,
                                send_data,
                                address,
                                retries,
                                wait_time,
                                seq_num,
                                MSG_TYPE_COMMAND,
                                moon_moon,
                                SECRET_KEY_INTERNAL,
                            ),
                            daemon=True,
                        ).start()

                elif command == video_3:

                    print("processing video_3")

                    if not config.connection_with_hopper:
                        print("video 3 unavailable")

                        threading.Thread(
                            target=secure_send_with_ack,
                            args=(
                                send_socket,
                                {
                                    message_type: sens,
                                    message_data: hopper_unavailable,
                                },
                                (EARTH_BASE_IP, EARTH_SEND_DATA_PORT_1),
                                retries,
                                wait_time,
                                seq_num,
                                MSG_TYPE_COMMAND,
                                earth_moon,
                                SECRET_KEY_INTERNAL,
                            ),
                            daemon=True,
                        ).start()

                    else:

                        send_data = {
                            message_type: video,
                        }

                        send_data.update({message_data: video_3})

                        config.asked_for_video = True
                        config.hopper_video = True

                        send_socket.settimeout(wait_time)
                        seq_num = random.randint(1, 1000000)
                        address = (LUNAR_HOPPER_IP, LUNAR_HOPPER_RECV_CMD_PORT)

                        threading.Thread(
                            target=secure_send_with_ack,
                            args=(
                                send_socket,
                                send_data,
                                address,
                                retries,
                                wait_time,
                                seq_num,
                                MSG_TYPE_COMMAND,
                                moon_moon,
                                SECRET_KEY_INTERNAL,
                            ),
                            daemon=True,
                        ).start()

            except Exception:
                continue

        else:
            time.sleep(0.1)


def get_nack_for_video(recv_sock):
    while True:
        while not config.connection_with_earth:
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
                address = (EARTH_BASE_IP, EARTH_RECIEVE_VIDEO_PORT)

                if recieved_type == nak:

                    p = Process(
                        target=secure_send,
                        args=(
                            payload,
                            recv_sock,
                            video_to_send[payload],
                            address,
                            MSG_TYPE_VIDEO,
                            earth_moon,
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
