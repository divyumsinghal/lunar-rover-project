from utils.make_packet import make_packet, parse_packet


def secure_send(seq_num, sock, data, addr):
    packet = make_packet(seq_num, data)
    sent = False

    try:
        sock.sendto(packet, addr)
    except Exception as e:
        print("[ERROR secure_send] Exception while sending data:", e)
