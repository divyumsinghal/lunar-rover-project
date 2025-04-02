import threading
import socket
from lunar_rover.config import *
from lunar_rover.earth_receive import (
    receive_data_from_earth_1,
    receive_data_from_earth_2,
    receive_data_from_earth_3,
    receive_data_from_earth_4,
)
from lunar_rover.earth_send import (
    send_data_to_earth_1,
    send_data_to_earth_2,
    send_data_to_earth_3,
    send_data_to_earth_4,
)
from lunar_rover.handshake import (
    handshake_rover_earth,
    handshake_rover_tunneller,
    handshake_rover_hopper,
)
from lunar_rover.send_video import send_video_to_earth, get_nack_for_video
from lunar_rover.recieve_video import (
    receive_video_from_tunneller_1,
    send_naks_for_video,
)

# Sending data to Earth Base
send_data_to_earth_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_earth_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_earth_socket_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_earth_socket_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

send_data_to_earth_socket_1.bind((LUNAR_ROVER_1_IP, 0))
send_data_to_earth_socket_2.bind((LUNAR_ROVER_1_IP, 0))
send_data_to_earth_socket_3.bind((LUNAR_ROVER_1_IP, 0))
send_data_to_earth_socket_4.bind((LUNAR_ROVER_1_IP, 0))

# Receiving data from Earth Base
receive_data_from_earth_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_earth_socket_1.bind((LUNAR_ROVER_1_IP, EARTH_RECEIVE_CMD_PORT_1))

receive_data_from_earth_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_earth_socket_2.bind((LUNAR_ROVER_1_IP, EARTH_RECEIVE_CMD_PORT_2))

receive_data_from_earth_socket_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_earth_socket_3.bind((LUNAR_ROVER_1_IP, EARTH_RECEIVE_CMD_PORT_3))

receive_data_from_earth_socket_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_data_from_earth_socket_4.bind((LUNAR_ROVER_1_IP, EARTH_RECEIVE_CMD_PORT_4))

# Sending Messages to tunneller
send_data_to_tunneller_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_tunneller_socket.bind((LUNAR_ROVER_1_IP, 0))
# Sending video to Earth Base
send_video_to_earth_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_video_to_earth_socket.bind((LUNAR_ROVER_1_IP, SEND_VIDEO_PORT))

# Recieving video from tunneller
recieve_video_from_tunneller_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_video_from_tunneller_socket.bind((LUNAR_ROVER_1_IP, ROVER_RECIEVE_VIDEO_PORT))

# Handshake
handshake_socket_earth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
handshake_socket_earth.bind((LUNAR_ROVER_1_IP, LUNAR_ROVER_HANDSHAKE_PORT_EARTH))

handshake_socket_tunneller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
handshake_socket_tunneller.bind(
    (LUNAR_ROVER_1_IP, LUNAR_ROVER_HANDSHAKE_PORT_TUNNELLER)
)

# Reciver Naks for video
nack_socket_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nack_socket_recv.bind((LUNAR_ROVER_1_IP, LUNAR_ROVER_VIDEO_NACK_PORT))

nack_socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nack_socket_send.bind((LUNAR_ROVER_1_IP, 0))

stop_event = threading.Event()


def main():

    print(f"[LUNAR ROVER] : Initiating Communication With EARTH BASE")

    # Handshake with EARTH_BASE & LUNAR_TUNNELLER
    threading.Thread(
        target=handshake_rover_earth,
        args=(handshake_socket_earth,),
        daemon=True,
    ).start()

    threading.Thread(
        target=handshake_rover_tunneller,
        args=(handshake_socket_tunneller,),
        daemon=True,
    ).start()

    threading.Thread(
        target=handshake_rover_hopper,
        args=(handshake_socket_tunneller,),
        daemon=True,
    ).start()

    # Receiving data from Earth Base
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
        target=receive_data_from_earth_3,
        args=(receive_data_from_earth_socket_3,),
        daemon=True,
    ).start()

    threading.Thread(
        target=receive_data_from_earth_4,
        args=(receive_data_from_earth_socket_4,),
        daemon=True,
    ).start()

    # Sending data to Earth Base
    threading.Thread(
        target=send_data_to_earth_1, args=(send_data_to_earth_socket_1,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_earth_2, args=(send_data_to_earth_socket_2,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_earth_3, args=(send_data_to_earth_socket_3,), daemon=True
    ).start()

    threading.Thread(
        target=send_data_to_earth_4, args=(send_data_to_earth_socket_4,), daemon=True
    ).start()

    # Send video to Earth Base
    threading.Thread(
        target=send_video_to_earth, args=(send_video_to_earth_socket,), daemon=True
    ).start()

    # Recv Naks for Video
    threading.Thread(
        target=get_nack_for_video,
        args=(nack_socket_recv,),
        daemon=True,
    ).start()

    # Send Naks for Video
    threading.Thread(
        target=send_naks_for_video,
        args=(
            nack_socket_send,
            (LUNAR_TUNNELLER_IP, LUNAR_TUNNELLER_VIDEO_NACK_PORT),
            (LUNAR_HOPPER_IP, LUNAR_HOPPER_VIDEO_NACK_PORT),
        ),
        daemon=True,
    ).start()

    # recieve video from tunneller and forward to Earth Base
    threading.Thread(
        target=receive_video_from_tunneller_1,
        args=(recieve_video_from_tunneller_socket, send_video_to_earth_socket),
        daemon=True,
    ).start()

    try:
        stop_event.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down the Rover...")
        stop_event.set()


if __name__ == "__main__":
    main()
