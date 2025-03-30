import reedsolo
import hmac
import hashlib

rs = reedsolo.RSCodec(100)


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


def encode_data(data):
    try:
        return rs.encode(data)
    except (TypeError, ValueError) as e:
        print(f"[ERROR encode_data] Invalid data for Reed-Solomon encoding: {e}")
        return None
    except Exception as e:
        print(f"[ERROR encode_data] Failed to encode data: {e}")
        return None


def decode_data(data):
    try:
        decoded_result = rs.decode(data)
        if isinstance(decoded_result, tuple):
            decoded_bytes = decoded_result[0]
        else:
            decoded_bytes = decoded_result
        return decoded_bytes
    except reedsolo.ReedSolomonError as e:
        print(f"[ERROR decode_data] Reed-Solomon unable to recover data: {e}")
        return None
    except (TypeError, ValueError) as e:
        print(f"[ERROR decode_data] Invalid data for Reed-Solomon decoding: {e}")
        return None
    except Exception as e:
        print(f"[ERROR decode_data] Unexpected error during decoding: {e}")
        return None
