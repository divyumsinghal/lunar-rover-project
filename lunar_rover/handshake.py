import time
import socket
from lunar_rover.config import *
from utils.client_server_comm import secure_receive, secure_send, secure_send_with_ack
import lunar_rover.config as config
import msgpack


def handshake_rover_earth(
    recv_socket,
    send_socket,
    tunneller_hadshake_port,
):
    print(
        f"[ROVER - handshake_rover_earth] Handshaking from rover on {LUNAR_ROVER_1_IP}"
    )

    seq_num = 0
    seq_num_tun = 0
    address_tunneller = (LUNAR_TUNNELLER_IP, tunneller_hadshake_port)
    recv_socket.settimeout(handshake_timeout)

    while True:
        try:
            seq_num, recv_data, addr = secure_receive(
                recv_socket,
                packet_type=MSG_TYPE_HANDSHAKE,
                # SECRET_KEY=SECRET_KEY_EARTH_ROVER,
            )

            if recv_data is None:
                print(f"[ROVER - handshake_rover_earth] Handshake failed")
                config.connection_with_earth = False
                continue

            message = msgpack.unpackb(recv_data, raw=False)
            recieved_type = message.get(message_type)

            if message is None:
                print(f"[ROVER - handshake_rover_earth] Handshake failed")
                config.connection_with_earth = False
                continue

            if recieved_type == handshake:
                print(f"[ROVER - handshake_rover_earth] Handshake successful")
                config.connection_with_earth = True

                ack_message = {
                    message_type: ack,
                    message_data: f"Received {handshake}",
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

        except socket.timeout:
            print(f"[ROVER - handshake_rover_earth] Handshake timed out. Waiting...")
            config.connection_with_earth = False
            continue

        except Exception as e:
            print(f"[ERROR andshake_rover_eart] Failed to send data: {e}")
