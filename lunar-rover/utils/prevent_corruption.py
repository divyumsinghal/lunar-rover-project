import reedsolo

rs = reedsolo.RSCodec(10)

SECRET_KEY = b"SUPER_SECRET_ROVER_KEY"


def encode_data(data):
    return rs.encode(data)


def decode_data(data):
    try:
        decoded_result = rs.decode(data)

        if isinstance(decoded_result, tuple):
            decoded_bytes = decoded_result[0]
        else:
            decoded_bytes = decoded_result
        return decoded_bytes

    except reedsolo.ReedSolomonError:
        print("[ERROR] Reed–Solomon unable to recover data.")
        return None
