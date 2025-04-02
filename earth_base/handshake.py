import time
from earth_base.config import *
from utils.client_server_comm import secure_send_with_ack
import earth_base.config as config


def handshake_earth_rover(send_socket, lunar_rover_IP, rover_hadshake_port):
    print(
        f"[EARTH - send_data_to_rover] Sending data to Lunar Rover on port {rover_hadshake_port}"
    )

    seq_num = 0
    send_socket.settimeout(wait_time)
    address = (lunar_rover_IP, rover_hadshake_port)

    while True:
        try:
            config.connection_with_rover = secure_send_with_ack(
                send_socket,
                {message_type: handshake, message_data: seq_num + 1},
                address,
                retries,
                wait_time,
                seq_num,
                MSG_TYPE_HANDSHAKE,
                earth_moon,
                SECRET_KEY=SECRET_KEY_INTERNAL,
            )

            if not config.connection_with_rover:
                print(f"[EARTH - handshake_earth_rover] Handshake failed")
            else:
                print(f"[EARTH - handshake_earth_rover] Handshake successful")

            if not config.immediately_check_connection_with_rover:
                time.sleep(handshake_interval)
            else:
                config.immediately_check_connection_with_rover = False

        except Exception as e:
            print(f"[ERROR handshake_earth_rover] Failed to send data: {e}")
