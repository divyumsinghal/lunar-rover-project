import socket
import msgpack
import random
import asyncio
from earth_base.config import *
from utils.client_server_comm import secure_receive, secure_send
import earth_base.config as config


def send_data_to_rover(send_socket):
    print(
        f"[EARTH - send_data_to_rover] Sending data to Lunar Rover on port {LUNAR_ROVER_SEND_DATA_PORT}"
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    pending_tasks = set()

    def handle_task_done(task):
        pending_tasks.discard(task)
        # Handle exceptions if needed
        if task.exception():
            print(f"[ERROR] Task raised exception: {task.exception()}")

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

                for attempt in range(retries):
                    attempt += 1
                    seq_num = random.randint(1, 1000000)
                    packed_data = msgpack.packb(CMD_data, use_bin_type=True)

                    task = loop.create_task(
                        secure_send(
                            seq_num,
                            send_socket,
                            packed_data,
                            (LUNAR_ROVER_1_IP, LUNAR_ROVER_SEND_DATA_PORT),
                        )
                    )

                    pending_tasks.add(task)
                    task.add_done_callback(handle_task_done)

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

        loop.run_until_complete(asyncio.sleep(0.1))
