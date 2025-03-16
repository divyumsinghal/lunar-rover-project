import msgpack
from src.config import *
from utils.client_server_comm import secure_send, secure_receive


def receive_data_from_rover(recv_socket):
    print(f"[EARTH BASE - RECEIVE] Listening on port {EARTH_RECEIVE_CMD_PORT}")

    while True:
        try:
            seq_num, data_bytes, addr = secure_receive(recv_socket)

            print(f"[LUNAR ROVER - RECEIVE] Recieving on port {EARTH_RECEIVE_CMD_PORT}")

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
                secure_send(seq_num, recv_socket, packed_ack, addr)

        except Exception as e:
            print(f"[ERROR receive_data_from_rover] Failed to receive data: {e}")
