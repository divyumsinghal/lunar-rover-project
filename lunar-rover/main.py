import threading
import socket
from src.config import *
from src.earth_receive import receive_data_from_earth
from src.earth_send import send_data_to_earth
from src.send_video import send_video_to_earth


send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((LOCAL_IP, SEND_VIDEO_PORT))

recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind((LOCAL_IP, EARTH_RECEIVE_CMD_PORT))

stop_event = threading.Event()


def main():

    print(f"[LUNAR ROVER] : Initiating Communication With EARTH BASE")

    threading.Thread(
        target=receive_data_from_earth, args=(recv_socket,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_earth, args=(send_socket,), daemon=True
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
