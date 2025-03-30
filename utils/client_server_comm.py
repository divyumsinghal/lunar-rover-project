from utils.make_packet import make_packet, parse_packet
from utils.simulate import simulate_channel
import socket
from utils.config import *


def secure_send(seq_num, sock, data, addr, packet_type=MSG_TYPE_COMMAND):
    try:
        # Add packet type to the sequence number
        combined_seq = (packet_type << 28) | (
            seq_num & 0x0FFFFFFF
        )  # Use top 4 bits for type
        packet = make_packet(combined_seq, data)

        packet = simulate_channel(packet)

        if packet is None:
            print(f"Packet was lost in transmission.")
            return

        sock.sendto(packet, addr)

    except socket.timeout:
        print("[ERROR secure_send] Timeout while sending data.")
    except socket.error as e:
        print(f"[ERROR secure_send] Socket error while sending data: {e}")
    except Exception as e:
        print(f"[ERROR secure_send] Unexpected error while sending data: {e}")


def secure_receive(sock, packet_type=None):
    try:
        while True:
            packet, addr = sock.recvfrom(65535)
            seq_num, data = parse_packet(packet)

            if seq_num is not None:
                # Extract packet type and actual sequence number
                received_type = (seq_num >> 28) & 0xF  # Extract top 4 bits
                actual_seq = seq_num & 0x0FFFFFFF  # Extract bottom 28 bits

                # If no specific type is requested or types match, process the packet
                if packet_type is None or received_type == packet_type:
                    if data is not None:
                        print(
                            f"[SUCCESS] Received packet {actual_seq} (type {received_type}) from {addr}."
                        )
                        return actual_seq, data, addr
                    else:
                        print(
                            f"[ERROR secure_receive] Failed to decode packet {actual_seq} (type {received_type})."
                        )
                        return None, None, addr
                else:
                    print(
                        f"[DEBUG] Ignoring packet of type {received_type}, waiting for type {packet_type}"
                    )
            else:
                print("[ERROR secure_receive] Failed to parse packet header.")
                return None, None, addr

    except socket.timeout:
        print("[ERROR secure_receive] Timeout while receiving data.")
        return None, None, None
    except socket.error as e:
        print(f"[ERROR secure_receive] Socket error while receiving data: {e}")
        return None, None, None
    except Exception as e:
        print(f"[ERROR secure_receive] Unexpected error while receiving data: {e}")
        return None, None, None
