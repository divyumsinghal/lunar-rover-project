import struct
from utils.compress import compress_data, decompress_data
from utils.prevent_corruption import (
    generate_hmac,
    verify_hmac,
    encode_data,
    decode_data,
)


def make_packet(seq_num, data, SECRET_KEY):
    try:
        hmac_value = generate_hmac(data, SECRET_KEY)
        data_with_hmac = hmac_value + data
        compressed_data = compress_data(data_with_hmac)
        encoded_data = encode_data(compressed_data)
        packet = struct.pack("!I", seq_num) + encoded_data
        return packet
    except struct.error as e:
        print(f"[ERROR make_packet] Failed to pack sequence number: {e}")
        return None
    except Exception as e:
        print(f"[ERROR make_packet] Failed to create packet: {e}")
        return None


def parse_packet(packet, SECRET_KEY):
    try:
        if len(packet) < 4:
            print("[ERROR parse_packet] Incomplete packet received.")
            return None, None

        seq_num = struct.unpack("!I", packet[:4])[0]
        encoded_data = packet[4:]

        try:
            decoded_bytes = decode_data(encoded_data)
            if decoded_bytes is None:
                print(
                    f"[ERROR decode_data] Failed to decode packet {seq_num}. Possible corruption!"
                )
                return seq_num, None
        except Exception as e:
            print(f"[ERROR decode_data] Exception while decoding packet {seq_num}: {e}")
            return seq_num, None

        try:
            decompressed_data = decompress_data(decoded_bytes)
            if decompressed_data is None:
                print(f"[ERROR decompress_data] Failed to decompress packet {seq_num}.")
                return seq_num, None
        except Exception as e:
            print(
                f"[ERROR decompress_data] Exception while decompressing packet {seq_num}: {e}"
            )
            return seq_num, None

        if len(decompressed_data) < 32:
            print(
                f"[ERROR parse_packet] Packet {seq_num} is too short to contain a valid HMAC."
            )
            return seq_num, None

        # Extract original data and HMAC
        original_data = decompressed_data[32:]
        received_hmac = decompressed_data[:32]

        try:
            if not verify_hmac(original_data, received_hmac, SECRET_KEY):
                print(
                    f"[ERROR verify_hmac] HMAC verification failed for packet {seq_num}. Possible tampering detected!"
                )
                return seq_num, None
        except Exception as e:
            print(
                f"[ERROR verify_hmac] Exception during HMAC verification for packet {seq_num}: {e}"
            )
            return seq_num, None

        print(f"[SUCCESS] Packet {seq_num} successfully received and verified.")
        return seq_num, original_data
    except struct.error as e:
        print(f"[ERROR parse_packet] Failed to unpack sequence number: {e}")
        return None, None
    except Exception as e:
        print(f"[ERROR parse_packet] Unexpected error while parsing packet: {e}")
        return None, None
