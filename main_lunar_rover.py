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
from lunar_rover.send_video import send_video_to_earth
from lunar_rover.recieve_video import receive_video_from_tunneller_1

# Sending data to Earth Base
send_data_to_earth_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_earth_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_earth_socket_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_data_to_earth_socket_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

# Sending video to Earth Base
send_video_to_earth_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_video_to_earth_socket.bind((LUNAR_ROVER_1_IP, SEND_VIDEO_PORT))

# Recieving video from tunneller
recieve_video_from_tunneller_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_video_from_tunneller_socket.bind((LUNAR_ROVER_1_IP, ROVER_RECIEVE_VIDEO_PORT))


stop_event = threading.Event()


def main():

    print(f"[LUNAR ROVER] : Initiating Communication With EARTH BASE")

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
