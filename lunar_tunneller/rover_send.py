import random
import threading
from lunar_tunneller.config import *
from utils.client_server_comm import *
import lunar_tunneller.config as config
import time


def send_data_to_rover(send_socket):
    print(
        f"[send_data_to_rover - SEND] Sending data to ROVER Base on port {TO_ROVER_TUNNELLER_SEND_DATA_PORT}"
    )

    while True:

        while not config.connection_with_rover:
            # print("[send_data_to_rover - SEND] Waiting for connection with rover...")
            time.sleep(0.5)

        if not command_queue.empty():
            try:

                sensor_data = {
                    message_type: cmd,
                }

                command = command_queue.get()

                if command == soil_moisture:
                    sensor_data.update({message_data: soil_moisture_sent + " " + "0"})
                    print(
                        f"[LUNAR TUNNELLER - send_data_to_rover] Command Queue: {command}"
                    )
                elif command == soil_pH:
                    sensor_data.update(
                        {message_data: soil_pH_sent + " " + str(random.randint(7, 10))}
                    )
                    print(
                        f"[LUNAR TUNNELLER - send_data_to_rover] Command Queue: {command}"
                    )
                elif command == soil_temp:
                    sensor_data.update(
                        {
                            message_data: soil_temp_sent
                            + " "
                            + str(random.uniform(1e-12, 1e-8))
                        }
                    )
                    print(
                        f"[LUNAR TUNNELLER - send_data_to_rover] Command Queue: {command}"
                    )
                elif command == soil_conductivity:
                    sensor_data.update(
                        {
                            message_data: soil_conductivity_sent
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
                address = (LUNAR_ROVER_1_IP, EARTH_RECEIVE_CMD_PORT_1)

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
                        SECRET_KEY_INTERNAL,
                    ),
                    daemon=True,
                ).start()

            except Exception as e:
                print(f"[ERROR send_data_to_earth] Failed to send data: {e}")
