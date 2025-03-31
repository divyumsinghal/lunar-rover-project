import time
from earth_base.config import *
from utils.client_server_comm import secure_receive, secure_send
import earth_base.config as config
import random
import msgpack


def receive_video_from_rover_1(recv_socket):
    print(f"[EARTH - RECEIVE] Listening for video on port {VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {recv_socket.getsockname()}")

    recv_socket.settimeout(None)

    print("[INFO] Waiting for video request to be sent to rover...")

    while not config.connection_with_rover:
        time.sleep(0.1)

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
                    video_to_store[int(timestamp)] = frame_data
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

    while not config.connection_with_rover:
        time.sleep(0.1)

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
                    video_to_store[int(timestamp)] = frame_data
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

    while not config.connection_with_rover:
        time.sleep(0.1)

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
                    video_to_store[int(timestamp)] = frame_data

                except Exception as e:
                    print(f"[ERROR] Failed to add frame to queue: {e}")

    except KeyboardInterrupt:
        print("[INFO] Video receiving stopped by user")
    except Exception as e:
        print(f"[ERROR] Fatal error in video receiving: {e}")
        import traceback

        traceback.print_exc()


def send_naks_for_video(send_sock, address):
    print(f"[EARTH - SEND] Listening for video on port {VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {send_sock.getsockname()}")

    send_sock.settimeout(None)

    while True:
        time.sleep(0.5)
        if not config.connection_with_rover:
            continue

        seq_num = random.randint(1, 1000000)
        if video_to_store:
            all_timestamps = sorted(video_to_store.keys())
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
                )
        except Exception as e:
            print(f"[ERROR] Failed to send NAK: {e}")
