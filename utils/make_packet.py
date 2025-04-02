import struct
from utils.compress import compress_data, decompress_data
from utils.prevent_corruption import (
    generate_hmac,
    verify_hmac,
    encode_data,
    decode_data,
    spread_packet,
    remake_packet,
)
from utils.security import xor_encrypt, xor_decrypt
from utils.config import *


def make_packet(seq_num, data, SECRET_KEY, ENCRYPTION_KEY=ENCRYPTION_KEY_DUMMY):
    try:
        compressed_data = compress_data(data)
        encrypted_data = xor_encrypt(compressed_data, ENCRYPTION_KEY)
        hmac_value = generate_hmac(encrypted_data, SECRET_KEY)
        data_with_hmac = hmac_value + encrypted_data
        encoded_data = encode_data(data_with_hmac)
        packet = struct.pack("!I", seq_num) + encoded_data
        spreaded_packet = spread_packet(packet)
        if spreaded_packet is None:
            print(f"[ERROR make_packet] Failed to transpose packet {seq_num}.")
            return None
        return spreaded_packet
    except struct.error as e:
        print(f"[ERROR make_packet] Failed to pack sequence number: {e}")
        return None
    except Exception as e:
        print(f"[ERROR make_packet] Failed to create packet: {e}")
        return None


def parse_packet(packet, SECRET_KEY, ENCRYPTION_KEY=ENCRYPTION_KEY_DUMMY):
    try:
        if len(packet) < 4:
            print("[ERROR parse_packet] Incomplete packet received.")
            return None, None

        original_packet = remake_packet(packet)
        if original_packet is None:
            print("[ERROR parse_packet] Failed to remake packet.")
            return None, None

        seq_num = struct.unpack("!I", original_packet[:4])[0]
        encoded_data = original_packet[4:]

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

        # Extract original data and HMAC
        encrypted_data = decoded_bytes[32:]
        received_hmac = decoded_bytes[:32]

        try:
            if not verify_hmac(encrypted_data, received_hmac, SECRET_KEY):
                # print(
                #    f"[ERROR verify_hmac] HMAC verification failed for packet {seq_num}. Possible tampering detected!"
                # )
                return seq_num, None
        except Exception as e:
            print(
                f"[ERROR verify_hmac] Exception during HMAC verification for packet {seq_num}: {e}"
            )
            return seq_num, None

        try:
            compressed_data = xor_decrypt(encrypted_data, ENCRYPTION_KEY)

            if compressed_data is None:
                print(f"[ERROR xor_decrypt] Failed to decrypt packet {seq_num}.")
                return seq_num, None

        except Exception as e:
            print(
                f"[ERROR xor_decrypt] Exception while decrypting packet {seq_num}: {e}"
            )
            return seq_num, None

        try:
            decompressed_data = decompress_data(compressed_data)
            if decompressed_data is None:
                print(f"[ERROR decompress_data] Failed to decompress packet {seq_num}.")
                return seq_num, None
        except Exception as e:
            print(
                f"[ERROR decompress_data] Exception while decompressing packet {seq_num}: {e}"
            )
            return seq_num, None

        if len(decompressed_data) <= 0:
            print(f"[ERROR parse_packet] Packet {seq_num} is too short.")
            return seq_num, None

        # print(f"[SUCCESS] Packet {seq_num} successfully received and verified.")
        return seq_num, decompressed_data
    except struct.error as e:
        print(f"[ERROR parse_packet] Failed to unpack sequence number: {e}")
        return None, None
    except Exception as e:
        print(f"[ERROR parse_packet] Unexpected error while parsing packet: {e}")
        return None, None
