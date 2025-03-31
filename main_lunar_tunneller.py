import threading
import socket
from lunar_tunneller.tunneller_receive import receive_data_from_rover
from lunar_tunneller.rover_send import send_data_to_rover
from lunar_tunneller.send_video import send_video_to_rover
from lunar_tunneller.config import *

# Sending data to Lunar Rover
send_data_to_lunar_rover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Receiving data from Lunar Rover
receive_data_from_rover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_rover_socket.bind((LUNAR_TUNNELLER_IP, LUNAR_TUNNELLER_RECV_CMD_PORT))

# Sending video to Lunar Rover
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


stop_event = threading.Event()


def main():

    print(f"[LUNAR TUNNELLER] : Initiating Communication With Lunar Rover")

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
