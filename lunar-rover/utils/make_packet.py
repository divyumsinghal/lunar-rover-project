import struct
from utils.compress import compress_data, decompress_data
from utils.prevent_corruption import (
    generate_hmac,
    verify_hmac,
    encode_data,
    decode_data,
)


def make_packet(seq_num, data):
    compressed_data = compress_data(data)
    encoded_data = encode_data(compressed_data)
    hmac_value = generate_hmac(encoded_data)
    packet = struct.pack("!I", seq_num) + encoded_data + hmac_value
    return packet


def parse_packet(packet):
    if len(packet) < 36:
        print("[ERROR parse_packet] Incomplete packet received.")
        return None, None

    seq_num = struct.unpack("!I", packet[:4])[0]
    received_hmac = packet[-32:]
    encoded_data = packet[4:-32]

    if not verify_hmac(encoded_data, received_hmac):
        print(
            "[ERROR verify_hmac] HMAC verification failed. Possible tampering detected!"
        )
        return seq_num, None

    decoded_bytes = decode_data(encoded_data)
    if decoded_bytes is None:
        print(
            f"[ERROR decode_data] Failed to decode packet {seq_num}. Possible corruption!"
        )
        return seq_num, None

    decompressed_data = decompress_data(decoded_bytes)
    if decompressed_data is None:
        print(f"[ERROR decompress_data] Failed to decompress packet {seq_num}.")
        return seq_num, None

    print(f"[SUCCESS] Packet {seq_num} successfully received and verified.")
    return seq_num, decompressed_data
