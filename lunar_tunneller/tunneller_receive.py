import msgpack
from lunar_tunneller.config import *

from utils.client_server_comm import secure_send, secure_receive


def receive_data_from_rover(recv_socket):
    print(
        f"[LUNAR TUNNELLER - RECEIVE] Listening on port {LUNAR_TUNNELLER_RECV_CMD_PORT}"
    )

    while True:
        try:
            seq_num, data_bytes, addr = secure_receive(recv_socket)
            print(
                f"[LUNAR TUNNELLER - RECEIVE] Receiving on port {LUNAR_TUNNELLER_RECV_CMD_PORT}"
            )

            if data_bytes:
                message = msgpack.unpackb(data_bytes, raw=False)

                print(f"[LUNAR TUNNELLER - RECEIVE] Received data: {message}")

                recieved_type = message.get(message_type)
                payload = message.get(message_data)
                print(f"[EARTH COMM - INCOMING] {recieved_type}: {payload}")

                if recieved_type == cmd:
                    command_queue.put(payload)
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
                )

        except Exception as e:
            print(
                f"[ERROR LUNAR TUNNELLER receive_data_from_rover] Failed to receive data: {e}"
            )
