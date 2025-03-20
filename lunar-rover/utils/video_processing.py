import struct
from utils.compress import compress_data, decompress_data
from utils.prevent_corruption import (
    generate_hmac,
    verify_hmac,
    encode_data,
    decode_data,
)


def make_packet(timestamp, data):
    try:
        hmac_value = generate_hmac(data)
        data_with_hmac = data + hmac_value
        compressed_data = compress_data(data_with_hmac)
        encoded_data = encode_data(compressed_data)
        packet = struct.pack("!I", timestamp) + encoded_data
        return packet
    except struct.error as e:
        print(f"[ERROR make_packet] Failed to pack sequence number: {e}")
        return None
    except Exception as e:
        print(f"[ERROR make_packet] Failed to create packet: {e}")
        return None


def parse_packet(packet):
    try:
        if len(packet) < 4:
            print("[ERROR parse_packet] Incomplete packet received.")
            return None, None

        timestamp = struct.unpack("!I", packet[:4])[0]
        encoded_data = packet[4:]

        try:
            decoded_bytes = decode_data(encoded_data)
            if decoded_bytes is None:
                print(
                    f"[ERROR decode_data] Failed to decode packet {timestamp}. Possible corruption!"
                )
                return timestamp, None
        except Exception as e:
            print(
                f"[ERROR decode_data] Exception while decoding packet {timestamp}: {e}"
            )
            return timestamp, None

        try:
            decompressed_data = decompress_data(decoded_bytes)
            if decompressed_data is None:
                print(
                    f"[ERROR decompress_data] Failed to decompress packet {timestamp}."
                )
                return timestamp, None
        except Exception as e:
            print(
                f"[ERROR decompress_data] Exception while decompressing packet {timestamp}: {e}"
            )
            return timestamp, None

        if len(decompressed_data) < 32:
            print(
                f"[ERROR parse_packet] Packet {timestamp} is too short to contain a valid HMAC."
            )
            return timestamp, None

        # Extract original data and HMAC
        original_data = decompressed_data[:-32]
        received_hmac = decompressed_data[-32:]

        try:
            if not verify_hmac(original_data, received_hmac):
                print(
                    f"[ERROR verify_hmac] HMAC verification failed for packet {timestamp}. Possible tampering detected!"
                )
                return timestamp, None
        except Exception as e:
            print(
                f"[ERROR verify_hmac] Exception during HMAC verification for packet {timestamp}: {e}"
            )
            return timestamp, None

        print(f"[SUCCESS] Packet {timestamp} successfully received and verified.")
        return timestamp, original_data
    except struct.error as e:
        print(f"[ERROR parse_packet] Failed to unpack sequence number: {e}")
        return None, None
    except Exception as e:
        print(f"[ERROR parse_packet] Unexpected error while parsing packet: {e}")
        return None, None
