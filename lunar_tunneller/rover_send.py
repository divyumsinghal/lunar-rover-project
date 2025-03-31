import random
import threading
from lunar_tunneller.config import *
from utils.client_server_comm import *


def send_data_to_rover(send_socket):
    print(
        f"[send_data_to_rover - SEND] Sending data to ROVER Base on port {TO_ROVER_TUNNELLER_SEND_DATA_PORT}"
    )

    while True:
        if not command_queue.empty():
            try:

                sensor_data = {
                    message_type: sens,
                }

                command = command_queue.get()

                if command == soil_moisture:
                    sensor_data.update(
                        {message_data: temperature + " " + str(random.randint(-50, 50))}
                    )
                    print(
                        f"[LUNAR TUNNELLER - send_data_to_rover] Command Queue: {command}"
                    )
                elif command == soil_pH:
                    sensor_data.update(
                        {message_data: humidity + " " + str(random.randint(0, 14))}
                    )
                    print(
                        f"[LUNAR TUNNELLER - send_data_to_rover] Command Queue: {command}"
                    )
                elif command == soil_temp:
                    sensor_data.update(
                        {
                            message_data: soil_conductivity
                            + " "
                            + str(random.randint(0, 100))
                        }
                    )
                    print(
                        f"[LUNAR TUNNELLER - send_data_to_rover] Command Queue: {command}"
                    )
                elif command == soil_conductivity:
                    sensor_data.update(
                        {
                            message_data: soil_moisture
                            + " "
                            + str(random.randint(0, 100))
                        }
                    )
                    print(
                        f"[LUNAR TUNNELLER - send_data_to_rover] Command Queue: {command}"
                    )
                else:
                    sensor_data.update({message_data: invalid_command + " " + command})
                    print(f"[INFO send_data_to_earth] Invalid command: {command}")

                send_socket.settimeout(wait_time)
                seq_num = random.randint(1, 1000000)
                address = (EARTH_BASE_IP, EARTH_SEND_DATA_PORT_1)

                threading.Thread(
                    target=secure_send_with_ack,
                    args=(
                        send_socket,
                        sensor_data,
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
                print(f"[ERROR send_data_to_earth] Failed to send data: {e}")
