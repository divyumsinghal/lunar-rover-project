import socket
import msgpack
import threading
import random
from earth_base.config import *
from utils.client_server_comm import secure_send_with_ack
import earth_base.config as config


def send_data_to_rover(send_socket):
    print(
        f"[EARTH - send_data_to_rover] Sending data to Lunar Rover on port {LUNAR_ROVER_SEND_DATA_PORT}"
    )

    while True:
        if not command_queue.empty() or not video_queue.empty():
            try:

                if not command_queue.empty():
                    command = command_queue.get()
                    print(f"[EARTH - send_data_to_rover] Command Queue: {command}")
                    CMD_data = {f"{message_type}": f"{cmd}"}
                    CMD_data.update({message_data: command})

                elif not video_queue.empty():
                    command = video_queue.get()
                    print(f"[EARTH - send_data_to_rover] VIDEO Queue: {command}")
                    CMD_data = {message_type: video}
                    CMD_data.update({message_data: command})
                    config.asked_for_video = True

                send_socket.settimeout(wait_time)
                seq_num = random.randint(1, 1000000)
                address = (LUNAR_ROVER_1_IP, LUNAR_ROVER_SEND_DATA_PORT)

                threading.Thread(
                    target=secure_send_with_ack,
                    args=(
                        send_socket,
                        CMD_data,
                        address,
                        retries,
                        wait_time,
                        seq_num,
                        MSG_TYPE_SENSOR,
                        earth_moon,
                    ),
                    daemon=True,
                ).start()

            except Exception as e:
                print(f"[ERROR send_data_to_rover] Failed to send data: {e}")
