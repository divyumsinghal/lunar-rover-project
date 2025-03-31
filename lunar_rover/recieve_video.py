import time
import socket
from lunar_rover.config import *
from utils.client_server_comm import secure_receive, secure_send
import lunar_rover.config as config
import cv2
from multiprocessing import Process


def receive_video_from_tunneller_1(recv_socket, send_socket):
    print(f"[EARTH - RECEIVE] Listening for video on port {ROVER_RECIEVE_VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {recv_socket.getsockname()}")

    try:
        recv_socket.settimeout(20)

        while True:

            print("[INFO] Waiting for video request to be sent to rover...")
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
                            recv_socket, packet_type=MSG_TYPE_VIDEO
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

                video_to_send.clear()
                config.asked_for_video = False

            except Exception as e:
                print(f"[ERROR] Fatal error in video receiving: {e}")

    except KeyboardInterrupt:
        print("[INFO] Video receiving stopped by user")
    except Exception as e:
        print(f"[ERROR] Fatal error in video receiving: {e}")
        import traceback

        traceback.print_exc()
