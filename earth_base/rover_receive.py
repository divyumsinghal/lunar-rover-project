import msgpack
import time
from earth_base.config import *
from utils.client_server_comm import secure_send, secure_receive
import earth_base.config as config


def receive_data_from_rover_1(recv_socket):
    print(f"[EARTH BASE - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT_1}")

    while True:

        while not config.connection_with_rover:
            time.sleep(0.1)

        try:
            seq_num, data_bytes, addr = secure_receive(recv_socket)

            print(
                f"[EARTH COMM - RECEIVE] Recieving on port {EARTH_RECEIVE_CMD_PORT_1}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                ack_message = {
                    f"{message_type}": f"{ack}",
                    f"{message_data}": f"Received {recieved_type}",
                }
                packed_ack = msgpack.packb(ack_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=recv_socket,
                    data=packed_ack,
                    addr=addr,
                    packet_type=MSG_TYPE_ACK,
                    channel=earth_moon,
                )

                sensor_data_recv_queue.put({seq_num: payload})

        except Exception as e:
            print(f"[ERROR receive_data_from_rover] Failed to receive data: {e}")


def receive_data_from_rover_2(recv_socket):
    print(f"[EARTH BASE - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT_2}")

    while True:

        while not config.connection_with_rover:
            time.sleep(0.1)

        try:
            seq_num, data_bytes, addr = secure_receive(recv_socket)

            print(
                f"[LUNAR ROVER - RECEIVE] Recieving on port {EARTH_RECEIVE_CMD_PORT_2}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                ack_message = {
                    f"{message_type}": f"{ack}",
                    f"{message_data}": f"Received {recieved_type}",
                }
                packed_ack = msgpack.packb(ack_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=recv_socket,
                    data=packed_ack,
                    addr=addr,
                    packet_type=MSG_TYPE_ACK,
                    channel=earth_moon,
                )

                sensor_data_recv_queue.put({seq_num: payload})

        except Exception as e:
            print(f"[ERROR receive_data_from_rover] Failed to receive data: {e}")


def receive_data_from_rover_3(recv_socket):
    print(f"[EARTH BASE - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT_3}")

    while True:

        while not config.connection_with_rover:
            time.sleep(0.1)

        try:
            seq_num, data_bytes, addr = secure_receive(recv_socket)

            print(
                f"[LUNAR ROVER - RECEIVE] Recieving on port {EARTH_RECEIVE_CMD_PORT_3}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                ack_message = {
                    f"{message_type}": f"{ack}",
                    f"{message_data}": f"Received {recieved_type}",
                }
                packed_ack = msgpack.packb(ack_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=recv_socket,
                    data=packed_ack,
                    addr=addr,
                    packet_type=MSG_TYPE_ACK,
                    channel=earth_moon,
                )

                sensor_data_recv_queue.put({seq_num: payload})

        except Exception as e:
            print(f"[ERROR receive_data_from_rover] Failed to receive data: {e}")


def receive_data_from_rover_4(recv_socket):
    print(f"[EARTH BASE - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT_4}")

    while True:

        while not config.connection_with_rover:
            time.sleep(0.1)

        try:
            seq_num, data_bytes, addr = secure_receive(recv_socket)

            print(
                f"[LUNAR ROVER - RECEIVE] Recieving on port {EARTH_RECEIVE_CMD_PORT_4}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)
                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                ack_message = {
                    f"{message_type}": f"{ack}",
                    f"{message_data}": f"Received {recieved_type}",
                }
                packed_ack = msgpack.packb(ack_message, use_bin_type=True)
                secure_send(
                    seq_num=seq_num,
                    sock=recv_socket,
                    data=packed_ack,
                    addr=addr,
                    packet_type=MSG_TYPE_ACK,
                    channel=earth_moon,
                )

                sensor_data_recv_queue.put({seq_num: payload})

        except Exception as e:
            print(f"[ERROR receive_data_from_rover] Failed to receive data: {e}")
