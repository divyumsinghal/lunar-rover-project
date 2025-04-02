import time
import socket
from lunar_rover.config import *
from utils.client_server_comm import secure_receive, secure_send, secure_send_with_ack
import lunar_rover.config as config
import msgpack


def handshake_rover_earth(
    recv_socket,
):
    print(
        f"[ROVER - handshake_rover_earth] Handshaking from rover on {LUNAR_ROVER_1_IP}"
    )

    seq_num = 0
    recv_socket.settimeout(handshake_timeout)

    while True:
        try:
            seq_num, recv_data, addr = secure_receive(
                recv_socket,
                packet_type=MSG_TYPE_HANDSHAKE,
                SECRET_KEY=SECRET_KEY_INTERNAL,
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
                    SECRET_KEY=SECRET_KEY_INTERNAL,
                )

        except socket.timeout:
            print(f"[ROVER - handshake_rover_earth] Handshake timed out. Waiting...")
            config.connection_with_earth = False
            continue

        except Exception as e:
            print(f"[ERROR handshake_rover_eart] Failed to send data: {e}")


def handshake_rover_tunneller(
    send_socket,
):
    print(
        f"[ROVER - handshake_rover_tunneller] Sending data to LUNAR_TUNNELLER_IP on port {LUNAR_TUNNELLER_IP}"
    )

    seq_num = 0
    send_socket.settimeout(wait_time)
    address = (LUNAR_TUNNELLER_IP, LUNAR_TUNNELLER_HANDSHAKE_PORT)

    while True:
        try:
            config.connection_with_tunneller = secure_send_with_ack(
                send_socket,
                {message_type: handshake, message_data: seq_num + 1},
                address,
                retries,
                wait_time,
                seq_num,
                MSG_TYPE_HANDSHAKE,
                moon_moon,
                SECRET_KEY=SECRET_KEY_INTERNAL,
            )

            if not config.connection_with_tunneller:
                print(f"[ROVER - handshake_rover_tunneller] Handshake failed")
            else:
                print(f"[ROVER - handshake_rover_tunneller] Handshake successful")

            if not config.immediately_check_connection_with_tunneller:
                time.sleep(handshake_interval)
            else:
                config.immediately_check_connection_with_tunneller = False

        except Exception as e:
            print(f"[ERROR handshake_rover_tunneller] Failed to send data: {e}")
