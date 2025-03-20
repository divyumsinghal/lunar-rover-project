import threading
import socket
from src.rover_receive import receive_data_from_rover
from src.rover_send import send_data_to_rover
from src.get_cmds import start_gui
from src.recieve_video import receive_video_from_rover
from src.config import *
from utils.simulate import process_packet_in_the_channel
from netfilterqueue import NetfilterQueue

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.bind((LOCAL_IP, EARTH_BASE_SEND_CMD_PORT))

recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind((LOCAL_IP, EARTH_RECEIVE_CMD_PORT))

video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((LOCAL_IP, VIDEO_PORT))
video_socket.connect((LUNAR_ROVER_1_IP, LUNAR_ROVER_RECIEVE_VIDEO_PORT))

stop_event = threading.Event()


def main():

    print(f"[EARTH BASE] : Initiating Communication With Rover")

    # nfqueue = NetfilterQueue()
    # nfqueue.bind(nf_queue_run, process_packet_in_the_channel)

    threading.Thread(
        target=receive_data_from_rover, args=(recv_socket,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_rover, args=(send_socket,), daemon=True
    ).start()

    # threading.Thread(
    #     target=receive_video_from_rover, args=(send_socket,), daemon=True
    # ).start()

    start_gui(command_queue=command_queue, video_queue=video_queue)

    try:
        # nfqueue.run()
        stop_event.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down Earth Base...")
        stop_event.set()
    # finally:
    # nfqueue.unbind()


if __name__ == "__main__":
    main()
