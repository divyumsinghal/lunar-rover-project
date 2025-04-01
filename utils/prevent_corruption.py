import reedsolo
import hmac
import hashlib
import numpy as np
import math

rs = reedsolo.RSCodec(12)


def generate_hmac(data, SECRET_KEY):
    try:
        return hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
    except TypeError as e:
        print(f"[ERROR generate_hmac] Invalid data type: {e}")
        return None
    except Exception as e:
        print(f"[ERROR generate_hmac] Failed to generate HMAC: {e}")
        return None


def verify_hmac(data, received_hmac, SECRET_KEY):
    try:
        calculated_hmac = generate_hmac(data, SECRET_KEY)
        if calculated_hmac is None:
            print("[ERROR verify_hmac] Failed to calculate HMAC for verification")
            return False
        return hmac.compare_digest(received_hmac, calculated_hmac)
    except TypeError as e:
        print(f"[ERROR verify_hmac] Invalid data type during HMAC comparison: {e}")
        return False
    except Exception as e:
        print(f"[ERROR verify_hmac] Failed to verify HMAC: {e}")
        return False


def encode_data(data, chunk_size=64, parity_bytes=12):
    try:
        rs = reedsolo.RSCodec(parity_bytes)
        encoded_data = bytearray()

        # Process data in chunks
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            encoded_chunk = rs.encode(chunk)  # Adds 12 parity bytes
            encoded_data.extend(encoded_chunk)

        return bytes(encoded_data)
    except (TypeError, ValueError) as e:
        print(f"[ERROR encode_data] Invalid data for Reed-Solomon encoding: {e}")
        return None
    except Exception as e:
        print(f"[ERROR encode_data] Failed to encode data: {e}")
        return None


def decode_data(data, chunk_size=64, parity_bytes=12):
    try:
        rs = reedsolo.RSCodec(parity_bytes)
        decoded_data = bytearray()

        # Process encoded data in chunks of (chunk_size + parity_bytes)
        for i in range(0, len(data), chunk_size + parity_bytes):
            chunk = data[i : i + chunk_size + parity_bytes]
            decoded_chunk = rs.decode(chunk)[0]
            decoded_data.extend(decoded_chunk)

        return bytes(decoded_data)

    except reedsolo.ReedSolomonError as e:
        print(f"[ERROR decode_data] Reed-Solomon unable to recover data: {e}")
        return None
    except (TypeError, ValueError) as e:
        print(f"[ERROR decode_data] Invalid data for Reed-Solomon decoding: {e}")
        return None
    except Exception as e:
        print(f"[ERROR decode_data] Unexpected error during decoding: {e}")
        return None


def spread_packet(packet: bytes) -> bytes:

    try:
        length = len(packet)
        rows = int(np.floor(np.sqrt(length)))
        cols = int(np.ceil(length / rows))

        padded_packet = packet + b"\x00" * (rows * cols - length)

        matrix = np.frombuffer(padded_packet, dtype=np.uint8).reshape(rows, cols)
        transpose = matrix.T.flatten().tobytes()

        # print( f"[DEBUG spread_packet] transposes  packet length: {len(transpose)}" )

        return transpose
    except ValueError as e:
        print(f"[ERROR spread_packet] ValueError: {e}")
        return None
    except Exception as e:
        print(f"[ERROR spread_packet] Unexpected error: {e}")
        return None


def remake_packet(transpose: bytes) -> bytes:

    try:
        length = len(transpose)
        rows = int(np.floor(np.sqrt(length)))
        cols = int(np.ceil(length / rows))

        if rows * cols != length:
            raise ValueError(
                f"Cannot reshape array of size {length} into shape ({rows}, {cols})"
            )

        matrix = np.frombuffer(transpose, dtype=np.uint8).reshape(cols, rows).T

        original_packet = matrix.flatten().tobytes()

        return original_packet.rstrip(b"\x00")

    except ValueError as e:
        print(f"[ERROR remake_packet] ValueError: {e}")
        return None
    except Exception as e:
        print(f"[ERROR remake_packet] Unexpected error: {e}")
        return None
