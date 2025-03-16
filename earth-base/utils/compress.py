import zlib


def compress_data(data):
    try:
        if isinstance(data, str):
            data = data.encode("utf-8")
        return zlib.compress(data)

    except zlib.error as e:
        print("[ERROR compress_data] Compression failed:", e)
        return None


def decompress_data(compressed_data):
    try:
        decompressed_bytes = zlib.decompress(compressed_data)
        return decompressed_bytes

    except zlib.error as e:
        print("[ERROR decompress_data] Decompression failed:", e)
        return None
