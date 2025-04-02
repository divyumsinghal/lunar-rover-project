import time
import socket
from lunar_rover.config import *
from utils.client_server_comm import secure_receive, secure_send
import lunar_rover.config as config
import cv2
from multiprocessing import Process
import random
import msgpack


def receive_video_from_tunneller_1(recv_socket, send_socket):
    print(f"[ROVER - RECEIVE] Listening for video on port {ROVER_RECIEVE_VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {recv_socket.getsockname()}")

    try:
        recv_socket.settimeout(wait_time)

        while True:

            print("[INFO] Waiting for video request to be sent to rover...")

            while not config.connection_with_tunneller:
                # print("[INFO] Waiting for connection with tunneller...")
                time.sleep(0.1)

            while not config.asked_for_video:
                time.sleep(0.5)

            print(
                "[INFO] Video request has been sent to tuneller, starting to receive frames"
            )

            try:

                frames_sent = 0
                while True:

                    try:
                        timestamp, frame_data, addr = secure_receive(
                            recv_socket,
                            packet_type=MSG_TYPE_VIDEO,
                            SECRET_KEY=SECRET_KEY_INTERNAL,
                        )

                    except socket.timeout:
                        print(
                            "[receive_video_from_tunneller_1] Video Reciving and Sending Over"
                        )
                        break

                    except Exception as e:
                        print(f"[ERROR] Exception in secure_receive: {e}")
                        continue

                    if timestamp is not None and frame_data is not None:

                        try:
                            address = (EARTH_BASE_IP, EARTH_RECIEVE_VIDEO_PORT)
                            try:
                                video_to_send[timestamp] = frame_data

                                p = Process(
                                    target=secure_send,
                                    args=(
                                        timestamp,
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

                                if frames_sent % 100 == 0:
                                    print(
                                        f"[ROVER - SEND] Sent frame {frames_sent} to Earth Base"
                                    )

                            except Exception as e:
                                print(
                                    f"[ERROR] Failed to send frame to Earth Base: {e}"
                                )
                                continue

                        except Exception as e:
                            print(f"[ERROR] Failed to add frame to queue: {e}")

                config.asked_for_video = False

                time.sleep(5)
                video_to_send.clear()

            except Exception as e:
                print(f"[ERROR] Fatal error in video receiving: {e}")

    except KeyboardInterrupt:
        print("[INFO] Video receiving stopped by user")
    except Exception as e:
        print(f"[ERROR] Fatal error in video receiving: {e}")
        import traceback

        traceback.print_exc()


def send_naks_for_video(send_sock, address):
    print(f"[ROVER - SEND] Listening for video on port {ROVER_RECIEVE_VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {send_sock.getsockname()}")

    send_sock.settimeout(None)

    while True:
        time.sleep(0.5)
        if not config.connection_with_tunneller:
            continue

        seq_num = random.randint(1, 1000000)
        if video_to_send:
            all_timestamps = sorted(video_to_send.keys())
            first_frame = all_timestamps[0]
            last_frame = all_timestamps[-1]
            expected_frames = set(range(first_frame, last_frame + 1))
            received_frames = set(all_timestamps)
            missing_frames = list(expected_frames - received_frames)
        else:
            missing_frames = []

        try:
            for missing_frame in missing_frames:
                nak_message = {message_type: nak, message_data: missing_frame}
                packed_message = msgpack.packb(nak_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=send_sock,
                    data=packed_message,
                    addr=address,
                    packet_type=MSG_TYPE_NAK,
                    channel=earth_moon,
                    SECRET_KEY=SECRET_KEY_INTERNAL,
                )
        except Exception as e:
            print(f"[ERROR] Failed to send NAK: {e}")
