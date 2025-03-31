import random
import threading
from lunar_rover.config import *
from utils.client_server_comm import *


def send_data_to_earth_1(send_socket):
    print(
        f"[EARTH COMM - SEND] Sending data to Earth Base on port {EARTH_SEND_DATA_PORT_1}"
    )

    while True:
        if not command_queue_1.empty():
            try:

                sensor_data = {
                    message_type: sens,
                }

                command = command_queue_1.get()

                if command == temperature:
                    sensor_data.update(
                        {message_data: temperature + " " + str(random.randint(-50, 50))}
                    )
                    print(f"[EARTH - send_data_to_earth] Command Queue: {command}")
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


def send_data_to_earth_2(send_socket):
    print(
        f"[EARTH COMM - SEND] Sending data to Earth Base on port {EARTH_SEND_DATA_PORT_2}"
    )

    while True:
        if not command_queue_2.empty():
            try:

                sensor_data = {
                    message_type: sens,
                }

                command = command_queue_2.get()

                if command == temperature:
                    sensor_data.update(
                        {message_data: temperature + " " + str(random.randint(-50, 50))}
                    )
                    print(f"[EARTH - send_data_to_earth] Command Queue: {command}")
                else:
                    sensor_data.update({message_data: invalid_command + " " + command})
                    print(f"[INFO send_data_to_earth] Invalid command: {command}")

                send_socket.settimeout(wait_time)
                seq_num = random.randint(1, 1000000)
                address = (EARTH_BASE_IP, EARTH_SEND_DATA_PORT_2)

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


def send_data_to_earth_3(send_socket):
    print(
        f"[EARTH COMM - SEND] Sending data to Earth Base on port {EARTH_SEND_DATA_PORT_3}"
    )

    while True:
        if not command_queue_3.empty():
            try:

                sensor_data = {
                    message_type: sens,
                }

                command = command_queue_3.get()

                if command == temperature:
                    sensor_data.update(
                        {message_data: temperature + " " + str(random.randint(-50, 50))}
                    )
                    print(f"[EARTH - send_data_to_earth] Command Queue: {command}")
                else:
                    sensor_data.update({message_data: invalid_command + " " + command})
                    print(f"[INFO send_data_to_earth] Invalid command: {command}")

                send_socket.settimeout(wait_time)
                seq_num = random.randint(1, 1000000)
                address = (EARTH_BASE_IP, EARTH_SEND_DATA_PORT_3)

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


def send_data_to_earth_4(send_socket):
    print(
        f"[EARTH COMM - SEND] Sending data to Earth Base on port {EARTH_SEND_DATA_PORT_4}"
    )

    while True:
        if not command_queue_4.empty():
            try:

                sensor_data = {
                    message_type: sens,
                }

                command = command_queue_4.get()

                if command == temperature:
                    sensor_data.update(
                        {message_data: temperature + " " + str(random.randint(-50, 50))}
                    )
                    print(f"[EARTH - send_data_to_earth] Command Queue: {command}")
                else:
                    sensor_data.update({message_data: invalid_command + " " + command})
                    print(f"[INFO send_data_to_earth] Invalid command: {command}")

                send_socket.settimeout(wait_time)
                seq_num = random.randint(1, 1000000)
                address = (EARTH_BASE_IP, EARTH_SEND_DATA_PORT_4)

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
