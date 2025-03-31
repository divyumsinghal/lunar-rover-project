import time
from earth_base.config import *
from utils.client_server_comm import secure_receive
import earth_base.config as config


def receive_video_from_rover_1(recv_socket):
    print(f"[EARTH - RECEIVE] Listening for video on port {VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {recv_socket.getsockname()}")

    recv_socket.settimeout(None)

    print("[INFO] Waiting for video request to be sent to rover...")
    while not config.asked_for_video:
        time.sleep(0.5)

    print("[INFO] Video request has been sent to rover, starting to receive frames")

    try:
        while True:
            try:
                timestamp, frame_data, addr = secure_receive(
                    recv_socket, packet_type=MSG_TYPE_VIDEO
                )
            except Exception as e:
                print(f"[ERROR] Exception in secure_receive: {e}")
                frames_dropped += 1
                continue

            if timestamp is not None and frame_data is not None:

                try:
                    play_frame_queue.put((int(timestamp), frame_data))
                except Exception as e:
                    print(f"[ERROR] Failed to add frame to queue: {e}")

    except KeyboardInterrupt:
        print("[INFO] Video receiving stopped by user")
    except Exception as e:
        print(f"[ERROR] Fatal error in video receiving: {e}")
        import traceback

        traceback.print_exc()


def receive_video_from_rover_2(recv_socket):
    print(f"[EARTH - RECEIVE] Listening for video on port {VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {recv_socket.getsockname()}")

    recv_socket.settimeout(None)

    print("[INFO] Waiting for video request to be sent to rover...")
    while not config.asked_for_video:
        time.sleep(0.5)

    print("[INFO] Video request has been sent to rover, starting to receive frames")

    try:
        while True:
            try:
                timestamp, frame_data, addr = secure_receive(
                    recv_socket, packet_type=MSG_TYPE_VIDEO
                )
            except Exception as e:
                print(f"[ERROR] Exception in secure_receive: {e}")
                frames_dropped += 1
                continue

            if timestamp is not None and frame_data is not None:

                try:
                    play_frame_queue.put((int(timestamp), frame_data))
                except Exception as e:
                    print(f"[ERROR] Failed to add frame to queue: {e}")

    except KeyboardInterrupt:
        print("[INFO] Video receiving stopped by user")
    except Exception as e:
        print(f"[ERROR] Fatal error in video receiving: {e}")
        import traceback

        traceback.print_exc()


def receive_video_from_rover_3(recv_socket):
    print(f"[EARTH - RECEIVE] Listening for video on port {VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {recv_socket.getsockname()}")

    recv_socket.settimeout(None)

    print("[INFO] Waiting for video request to be sent to rover...")
    while not config.asked_for_video:
        time.sleep(0.5)

    print("[INFO] Video request has been sent to rover, starting to receive frames")

    try:
        while True:
            try:
                timestamp, frame_data, addr = secure_receive(
                    recv_socket, packet_type=MSG_TYPE_VIDEO
                )
            except Exception as e:
                print(f"[ERROR] Exception in secure_receive: {e}")
                frames_dropped += 1
                continue

            if timestamp is not None and frame_data is not None:

                try:
                    play_frame_queue.put((int(timestamp), frame_data))
                except Exception as e:
                    print(f"[ERROR] Failed to add frame to queue: {e}")

    except KeyboardInterrupt:
        print("[INFO] Video receiving stopped by user")
    except Exception as e:
        print(f"[ERROR] Fatal error in video receiving: {e}")
        import traceback

        traceback.print_exc()
