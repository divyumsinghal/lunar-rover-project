import threading
import socket
from earth_base.rover_receive import (
    receive_data_from_rover_1,
    receive_data_from_rover_2,
)
from earth_base.rover_send import send_data_to_rover_1, send_data_to_rover_2
from earth_base.get_cmds import start_gui
from earth_base.recieve_video import (
    receive_video_from_rover_1,
    receive_video_from_rover_2,
    receive_video_from_rover_3,
)
from earth_base.config import *
from earth_base.video_player import video_playback

# from utils.simulate import process_packet_in_the_channel

# from netfilterqueue import NetfilterQueue

print(f"[INFO] Starting Earth Base with configuration:")
print(f"[INFO] - Local IP: {EARTH_BASE_IP}")
print(f"[INFO] - Rover IP: {LUNAR_ROVER_1_IP}")
print(f"[INFO] - Command receive port: {EARTH_RECEIVE_CMD_PORT_1}")
print(f"[INFO] - Video receive port: {VIDEO_PORT}")

send_data_to_rover_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_rover_socket_1.bind((EARTH_BASE_IP, EARTH_BASE_SEND_CMD_PORT_1))
print(
    f"[INFO] Command send socket bound to {send_data_to_rover_socket_1.getsockname()}"
)

send_data_to_rover_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_rover_socket_2.bind((EARTH_BASE_IP, EARTH_BASE_SEND_CMD_PORT_2))
print(
    f"[INFO] Command send socket bound to {send_data_to_rover_socket_2.getsockname()}"
)

receive_data_from_rover_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_rover_socket_1.bind((EARTH_BASE_IP, EARTH_RECEIVE_CMD_PORT_1))
print(
    f"[INFO] Command receive socket bound to {receive_data_from_rover_socket_1.getsockname()}"
)

receive_data_from_rover_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_rover_socket_2.bind((EARTH_BASE_IP, EARTH_RECEIVE_CMD_PORT_2))
print(
    f"[INFO] Command receive socket bound to {receive_data_from_rover_socket_2.getsockname()}"
)


video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((EARTH_BASE_IP, VIDEO_PORT))
print(f"[INFO] Video receive socket bound to {video_socket.getsockname()}")

stop_event = threading.Event()


def main():

    print(f"[EARTH BASE] : Initiating Communication With Rover")

    # nfqueue = NetfilterQueue()
    # nfqueue.bind(nf_queue_run, process_packet_in_the_channel)

    threading.Thread(
        target=receive_data_from_rover_1,
        args=(receive_data_from_rover_socket_1,),
        daemon=True,
    ).start()

    threading.Thread(
        target=receive_data_from_rover_2,
        args=(receive_data_from_rover_socket_2,),
        daemon=True,
    ).start()

    threading.Thread(
        target=send_data_to_rover_1, args=(send_data_to_rover_socket_1,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_rover_2, args=(send_data_to_rover_socket_2,), daemon=True
    ).start()

    threading.Thread(
        target=receive_video_from_rover_1, args=(video_socket,), daemon=True
    ).start()

    threading.Thread(
        target=receive_video_from_rover_2, args=(video_socket,), daemon=True
    ).start()

    threading.Thread(
        target=receive_video_from_rover_3, args=(video_socket,), daemon=True
    ).start()

    threading.Thread(target=video_playback, daemon=True).start()

    start_gui(
        command_queue_1=command_queue_1,
        command_queue_2=command_queue_2,
        video_queue=video_queue,
    )

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
