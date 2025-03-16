import struct
from utils.compress import compress_data
from utils.prevent_corruption import (
    generate_hmac,
    encode_data,
)


def make_packet(seq_num, data):
    compressed_data = compress_data(data)
    encoded_data = encode_data(compressed_data)
    hmac_value = generate_hmac(encoded_data)
    packet = struct.pack("!I", seq_num) + encoded_data + hmac_value
    return packet
