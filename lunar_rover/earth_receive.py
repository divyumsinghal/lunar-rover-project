import msgpack
import time
from lunar_rover.config import *
from utils.client_server_comm import secure_send, secure_receive
import lunar_rover.config as config


def receive_data_from_earth_1(recv_socket):
    print(f"[LUNAR ROVER - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT_1}")

    while True:

        try:

            while not config.connection_with_earth:
                time.sleep(0.1)

            seq_num, data_bytes, addr = secure_receive(
                recv_socket,
                SECRET_KEY=SECRET_KEY_INTERNAL,
            )
            print(
                f"[LUNAR ROVER - RECEIVE] Receiving on port {EARTH_RECEIVE_CMD_PORT_1}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                if recieved_type == cmd:
                    command_queue_1.put(payload)
                    print(f"[EARTH COMM - INCOMING] Command Queue Updated")

                elif recieved_type == video:
                    video_queue.put(payload)
                    print(f"[EARTH COMM - INCOMING] VIDEO Queue Updated")
                    print(video_queue)

                ack_message = {
                    message_type: ack,
                    message_data: f"Received {recieved_type}",
                }

                print(
                    f"Message received: {recieved_type}, sending Ack: {ack_message} to {addr}"
                )

                packed_ack = msgpack.packb(ack_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=recv_socket,
                    data=packed_ack,
                    addr=addr,
                    packet_type=MSG_TYPE_ACK,
                    channel=earth_moon,
                    SECRET_KEY=SECRET_KEY_INTERNAL,
                )

        except Exception as e:
            print(f"[ERROR receive_data_from_earth] Failed to receive data: {e}")


def receive_data_from_earth_2(recv_socket):
    print(f"[LUNAR ROVER - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT_2}")

    while True:
        try:

            while not config.connection_with_earth:
                time.sleep(0.1)

            seq_num, data_bytes, addr = secure_receive(
                recv_socket,
                SECRET_KEY=SECRET_KEY_INTERNAL,
            )
            print(
                f"[LUNAR ROVER - RECEIVE] Receiving on port {EARTH_RECEIVE_CMD_PORT_2}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                if recieved_type == cmd:
                    command_queue_2.put(payload)
                    print(f"[EARTH COMM - INCOMING] Command Queue Updated")

                ack_message = {
                    message_type: ack,
                    message_data: f"Received {recieved_type}",
                }

                print(
                    f"Message received: {recieved_type}, sending Ack: {ack_message} to {addr}"
                )

                packed_ack = msgpack.packb(ack_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=recv_socket,
                    data=packed_ack,
                    addr=addr,
                    packet_type=MSG_TYPE_ACK,
                    channel=earth_moon,
                    SECRET_KEY=SECRET_KEY_INTERNAL,
                )

        except Exception as e:
            print(f"[ERROR receive_data_from_earth] Failed to receive data: {e}")


def receive_data_from_earth_3(recv_socket):
    print(f"[LUNAR ROVER - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT_3}")

    while True:

        while not config.connection_with_earth:
            time.sleep(0.1)

        try:
            seq_num, data_bytes, addr = secure_receive(
                recv_socket,
                SECRET_KEY=SECRET_KEY_INTERNAL,
            )
            print(
                f"[LUNAR ROVER - RECEIVE] Receiving on port {EARTH_RECEIVE_CMD_PORT_3}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                if recieved_type == cmd:
                    command_queue_3.put(payload)
                    print(f"[EARTH COMM - INCOMING] Command Queue Updated")

                elif recieved_type == video:
                    video_queue.put(payload)
                    print(f"[EARTH COMM - INCOMING] VIDEO Queue Updated")
                    print(video_queue)

                ack_message = {
                    message_type: ack,
                    message_data: f"Received {recieved_type}",
                }

                print(
                    f"Message received: {recieved_type}, sending Ack: {ack_message} to {addr}"
                )

                packed_ack = msgpack.packb(ack_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=recv_socket,
                    data=packed_ack,
                    addr=addr,
                    packet_type=MSG_TYPE_ACK,
                    channel=earth_moon,
                    SECRET_KEY=SECRET_KEY_INTERNAL,
                )

        except Exception as e:
            print(f"[ERROR receive_data_from_earth] Failed to receive data: {e}")


def receive_data_from_earth_4(recv_socket):
    print(f"[LUNAR ROVER - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT_4}")

    while True:
        try:

            while not config.connection_with_earth:
                time.sleep(0.1)

            seq_num, data_bytes, addr = secure_receive(
                recv_socket,
                SECRET_KEY=SECRET_KEY_INTERNAL,
            )
            print(
                f"[LUNAR ROVER - RECEIVE] Receiving on port {EARTH_RECEIVE_CMD_PORT_4}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                if recieved_type == cmd:
                    command_queue_4.put(payload)
                    print(f"[EARTH COMM - INCOMING] Command Queue Updated")

                ack_message = {
                    message_type: ack,
                    message_data: f"Received {recieved_type}",
                }

                print(
                    f"Message received: {recieved_type}, sending Ack: {ack_message} to {addr}"
                )

                packed_ack = msgpack.packb(ack_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=recv_socket,
                    data=packed_ack,
                    addr=addr,
                    packet_type=MSG_TYPE_ACK,
                    channel=earth_moon,
                    SECRET_KEY=SECRET_KEY_INTERNAL,
                )

        except Exception as e:
            print(f"[ERROR receive_data_from_earth] Failed to receive data: {e}")
