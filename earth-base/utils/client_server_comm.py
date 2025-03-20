from utils.make_packet import make_packet, parse_packet
from utils.simulate import simulate_channel
import socket

max_packet_size = 4096


def secure_send(seq_num, sock, data, addr):
    try:

        # if data too much drop it
        if len(data) > max_packet_size:
            print(f"[ERROR secure_send] Packet size too large: {len(data)}")
            return

        packet = make_packet(seq_num, data)
        packet = simulate_channel(packet)
        sock.sendto(packet, addr)

    except socket.timeout:
        print("[ERROR secure_send] Timeout while sending data.")
    except socket.error as e:
        print(f"[ERROR secure_send] Socket error while sending data: {e}")
    except Exception as e:
        print(f"[ERROR secure_send] Unexpected error while sending data: {e}")


def secure_receive(sock):
    try:
        packet, addr = sock.recvfrom(65535)

        # if packet is too large drop it
        if len(packet) > max_packet_size:
            print(f"[ERROR secure_receive] Packet size too large: {len(packet)}")
            return None, None, None

        seq_num, data = parse_packet(packet)

        if data is not None:
            print(f"[SUCCESS] Received packet {seq_num} from {addr}.")
            return seq_num, data, addr
        else:
            print(f"[ERROR secure_receive] Failed to decode packet {seq_num}.")
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
