import random
import threading
from lunar_hopper.config import *
from utils.client_server_comm import *
import lunar_hopper.config as config
import time


def send_data_to_rover(send_socket):
    print(
        f"[send_data_to_rover - SEND] Sending data to ROVER Base on port {TO_ROVER_HOPPER_SEND_DATA_PORT}"
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

                if command == Total_Ionizing_Dose:
                    sensor_data.update(
                        {
                            message_data: Total_Ionizing_Dose_sent
                            + " "
                            + str(random.uniform(0.01, 0.1))
                        }
                    )
                    print(
                        f"[LUNAR HOPPER - send_data_to_rover] Command Queue: {command}"
                    )
                elif command == Dose_Rate:
                    sensor_data.update(
                        {
                            message_data: Dose_Rate_sent
                            + " "
                            + str(random.uniform(0.01, 0.1))
                        }
                    )
                    print(
                        f"[LUNAR HOPPER - send_data_to_rover] Command Queue: {command}"
                    )
                elif command == Particle_Flux:
                    sensor_data.update(
                        {
                            message_data: Particle_Flux_sent
                            + " "
                            + str(random.randint(10, 1000))
                        }
                    )
                    print(
                        f"[LUNAR HOPPER - send_data_to_rover] Command Queue: {command}"
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
