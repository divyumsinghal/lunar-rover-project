import threading
import socket
from earth_base.rover_receive import (
    receive_data_from_rover_1,
    receive_data_from_rover_2,
    receive_data_from_rover_3,
    receive_data_from_rover_4,
)
from earth_base.rover_send import (
    send_data_to_rover_1,
    send_data_to_rover_2,
    send_data_to_rover_3,
    send_data_to_rover_4,
)
from earth_base.get_cmds import start_gui
from earth_base.recieve_video import (
    receive_video_from_rover_1,
    receive_video_from_rover_2,
    receive_video_from_rover_3,
    send_naks_for_video,
)
from earth_base.handshake import handshake_earth_rover
from earth_base.config import *
from earth_base.video_player import video_playback

print(f"[INFO] Starting Earth Base with configuration:")
print(f"[INFO] - Local IP: {EARTH_BASE_IP}")
print(f"[INFO] - Rover IP: {LUNAR_ROVER_1_IP}")

# SEND DATA TO ROVER
send_data_to_rover_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_rover_socket_1.bind((EARTH_BASE_IP, EARTH_BASE_SEND_CMD_PORT_1))

send_data_to_rover_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_rover_socket_2.bind((EARTH_BASE_IP, EARTH_BASE_SEND_CMD_PORT_2))

send_data_to_rover_socket_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_rover_socket_3.bind((EARTH_BASE_IP, EARTH_BASE_SEND_CMD_PORT_3))

send_data_to_rover_socket_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_rover_socket_4.bind((EARTH_BASE_IP, EARTH_BASE_SEND_CMD_PORT_4))

# RECEIVE DATA FROM ROVER
receive_data_from_rover_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_rover_socket_1.bind((EARTH_BASE_IP, EARTH_RECEIVE_CMD_PORT_1))

receive_data_from_rover_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_rover_socket_2.bind((EARTH_BASE_IP, EARTH_RECEIVE_CMD_PORT_2))

receive_data_from_rover_socket_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_rover_socket_3.bind((EARTH_BASE_IP, EARTH_RECEIVE_CMD_PORT_3))

receive_data_from_rover_socket_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_rover_socket_4.bind((EARTH_BASE_IP, EARTH_RECEIVE_CMD_PORT_4))

# RECEIVE VIDEO FROM ROVER
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((EARTH_BASE_IP, VIDEO_PORT))
print(f"[INFO] Video receive socket bound to {video_socket.getsockname()}")

# Send Naks for video
nack_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Handshake
handshake_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
handshake_socket.bind((EARTH_BASE_IP, EARTH_BASE_HANDSHAKE_PORT))

stop_event = threading.Event()


def main():

    print(f"[EARTH BASE] : Initiating Communication With Rover")

    # Handshake with rover
    threading.Thread(
        target=handshake_earth_rover,
        args=(handshake_socket, LUNAR_ROVER_1_IP, LUNAR_ROVER_HANDSHAKE_PORT_EARTH),
        daemon=True,
    ).start()

    # Receiving data from rover
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
        target=receive_data_from_rover_3,
        args=(receive_data_from_rover_socket_3,),
        daemon=True,
    ).start()

    threading.Thread(
        target=receive_data_from_rover_4,
        args=(receive_data_from_rover_socket_4,),
        daemon=True,
    ).start()

    # Sending data to rover
    threading.Thread(
        target=send_data_to_rover_1, args=(send_data_to_rover_socket_1,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_rover_2, args=(send_data_to_rover_socket_2,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_rover_3, args=(send_data_to_rover_socket_3,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_rover_4, args=(send_data_to_rover_socket_4,), daemon=True
    ).start()

    # Recieving video from rover
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

    # Send Naks for Video
    threading.Thread(
        target=send_naks_for_video,
        args=(nack_socket, (LUNAR_ROVER_1_IP, LUNAR_ROVER_VIDEO_NACK_PORT)),
        daemon=True,
    ).start()

    start_gui(
        command_queue_1=command_queue_1,
        command_queue_2=command_queue_2,
        command_queue_3=command_queue_3,
        command_queue_4=command_queue_4,
        video_queue=video_queue,
    )

    try:
        stop_event.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down Earth Base...")
        stop_event.set()


if __name__ == "__main__":
    main()
