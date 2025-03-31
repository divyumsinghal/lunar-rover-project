import threading
import socket
from lunar_rover.config import *
from lunar_rover.earth_receive import (
    receive_data_from_earth_1,
    receive_data_from_earth_2,
)
from lunar_rover.earth_send import send_data_to_earth_1, send_data_to_earth_2
from lunar_rover.send_video import send_video_to_earth


send_data_to_earth_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_earth_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((LUNAR_ROVER_1_IP, SEND_VIDEO_PORT))

receive_data_from_earth_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_earth_socket_1.bind((LUNAR_ROVER_1_IP, EARTH_RECEIVE_CMD_PORT_1))

receive_data_from_earth_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_earth_socket_2.bind((LUNAR_ROVER_1_IP, EARTH_RECEIVE_CMD_PORT_2))


stop_event = threading.Event()


def main():

    print(f"[LUNAR ROVER] : Initiating Communication With EARTH BASE")

    threading.Thread(
        target=receive_data_from_earth_1,
        args=(receive_data_from_earth_socket_1,),
        daemon=True,
    ).start()

    threading.Thread(
        target=receive_data_from_earth_2,
        args=(receive_data_from_earth_socket_2,),
        daemon=True,
    ).start()

    threading.Thread(
        target=send_data_to_earth_1, args=(send_data_to_earth_socket_1,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_earth_2, args=(send_data_to_earth_socket_2,), daemon=True
    ).start()

    threading.Thread(
        target=send_video_to_earth, args=(video_socket,), daemon=True
    ).start()

    # threading.Thread(target=peer_receive_data, daemon=True).start()
    # threading.Thread(target=peer_send_data, daemon=True).start()

    try:
        stop_event.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down the Rover...")
        stop_event.set()


if __name__ == "__main__":
    main()
