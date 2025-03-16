import socket
import msgpack
import time
import random
from src.config import *
from utils.client_server_comm import secure_send, secure_receive


def send_data_to_earth(send_socket):

    print(
        f"[EARTH COMM - SEND] Sending data to Earth Base on port {EARTH_SEND_DATA_PORT}"
    )

    while True:

        if not command_queue.empty():
            try:

                sensor_data = {
                    f"{message_type}": f"{sens}",
                }

                command = command_queue.get()

                if command == temperature:
                    sensor_data.update({f"{message_data}": random.randint(-50, 50)})
                    print(f"[EARTH - send_data_to_earth] Command Queue: {command}")
                else:
                    print(f"[ERROR send_data_to_earth] Invalid command: {command}")
                    continue

                send_socket.settimeout(2)

                retries = 3

                for attempt in range(retries):
                    seq_num = random.randint(1, 1000000)
                    packed_data = msgpack.packb(sensor_data, use_bin_type=True)

                    secure_send(
                        seq_num,
                        send_socket,
                        packed_data,
                        (EARTH_BASE_IP, EARTH_SEND_DATA_PORT),
                    )

                    print(
                        f"[EARTH COMM - OUTGOING] Attempt {attempt + 1} Sent: {sensor_data}"
                    )

                    try:
                        print(f"[ROVER to Earth - OUTGOING] Sent: {sensor_data}")

                        ack_seq, ack_bytes, addr = secure_receive(send_socket)
                        if ack_bytes:
                            ack_message = msgpack.unpackb(ack_bytes, raw=False)
                            print(
                                f"[EARTH COMM - OUTGOING] ACK Received: {ack_seq} : {ack_message}"
                            )
                            break

                    except socket.timeout:
                        print(f"[WARNING] No ACK received retrying...")

            except Exception as e:
                print(f"[ERROR send_data_to_earth] Failed to send data: {e}")
