import threading
import socket
from lunar_hopper.rover_receive import receive_data_from_rover
from lunar_hopper.rover_send import send_data_to_rover
from lunar_hopper.send_video import send_video_to_rover, get_nack_for_video
from lunar_hopper.handshake import handshake_rover_hopper
from lunar_hopper.config import *

# Sending data to Lunar Rover
send_data_to_lunar_rover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_lunar_rover_socket.bind((LUNAR_HOPPER_IP, 0))

# Receiving data from Lunar Rover
receive_data_from_rover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_rover_socket.bind((LUNAR_HOPPER_IP, LUNAR_HOPPER_RECV_CMD_PORT))

# Sending video to Lunar Rover
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((LUNAR_HOPPER_IP, 0))

# handshake
handshake_socket_rover = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
handshake_socket_rover.bind((LUNAR_HOPPER_IP, LUNAR_HOPPER_HANDSHAKE_PORT))

# Nack
nack_socket_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nack_socket_recv.bind((LUNAR_HOPPER_IP, LUNAR_HOPPER_VIDEO_NACK_PORT))

stop_event = threading.Event()


def main():

    print(f"[LUNAR TUNNELLER] : Initiating Communication With Lunar Rover")

    # Handshake with & LUNAR_ROVER
    threading.Thread(
        target=handshake_rover_hopper,
        args=(handshake_socket_rover,),
        daemon=True,
    ).start()

    # Receiving data from Rover
    threading.Thread(
        target=receive_data_from_rover,
        args=(receive_data_from_rover_socket,),
        daemon=True,
    ).start()

    # Sending data to Rover
    threading.Thread(
        target=send_data_to_rover, args=(send_data_to_lunar_rover_socket,), daemon=True
    ).start()

    # Recv Naks for Video
    threading.Thread(
        target=get_nack_for_video,
        args=(nack_socket_recv,),
        daemon=True,
    ).start()

    # Send video to Rover
    threading.Thread(
        target=send_video_to_rover, args=(video_socket,), daemon=True
    ).start()

    try:
        stop_event.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down the Rover...")
        stop_event.set()


if __name__ == "__main__":
    main()
