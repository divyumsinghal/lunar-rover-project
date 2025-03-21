import socket
import msgpack
import time
import random
from src.config import *
from utils.client_server_comm import secure_receive, secure_send


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
                    asked_for_video = True

                send_socket.settimeout(wait_time)

                for attempt in range(retries):
                    attempt += 1
                    seq_num = random.randint(1, 1000000)
                    packed_data = msgpack.packb(CMD_data, use_bin_type=True)

                    secure_send(
                        seq_num,
                        send_socket,
                        packed_data,
                        (LUNAR_ROVER_1_IP, LUNAR_ROVER_SEND_DATA_PORT),
                    )

                    print(
                        f"[EARTH COMM - OUTGOING] Attempt {attempt} Sent: {CMD_data} {packed_data}"
                    )

                    try:
                        print(f"[ROVER to Earth - OUTGOING] Sent: {CMD_data}")
                        ack_seq, ack_bytes, addr = secure_receive(send_socket)

                        if ack_bytes:
                            ack_message = msgpack.unpackb(ack_bytes, raw=False)
                            print(
                                f"[EARTH COMM - OUTGOING] ACK Received: {ack_seq} : {ack_message}"
                            )
                            break

                    except socket.timeout:
                        print(f"[WARNING] No ACK received, retrying...")

            except Exception as e:
                print(f"[ERROR send_data_to_rover] Failed to send data: {e}")
