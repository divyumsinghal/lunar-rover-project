from utils.make_packet import make_packet, parse_packet


def secure_send(seq_num, sock, data, addr):
    packet = make_packet(seq_num, data)
    sent = False

    try:
        sock.sendto(packet, addr)
    except Exception as e:
        print("[ERROR secure_send] Exception while sending data:", e)


def secure_receive(sock):
    try:
        packet, addr = sock.recvfrom(4096)
        seq_num, data = parse_packet(packet)
        if data is not None:
            print(f"[SUCCESS] Received packet {seq_num} from {addr}.")
            return seq_num, data, addr
        else:
            print(f"[ERROR secure_receive] Failed to decode packet {seq_num}.")
            return None, None, addr
    except Exception as e:
        print("[ERROR secure_receive] Exception while receiving data:", e)
        return None, None, None
