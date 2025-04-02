from utils.config import *


def generate_keystream(key, length, seed=0):
    try:
        keystream = bytearray()
        key_len = len(key)

        for i in range(length):
            value = (key[i % key_len] ^ (i & 0xFF) ^ seed) & 0xFF
            keystream.append(value)

        return bytes(keystream)
    except Exception as e:
        print(f"Error in generate_keystream: {e}")
        return b""


def xor_encrypt(data, key=ENCRYPTION_KEY_DUMMY, block_size=64):
    try:
        padding_len = (block_size - (len(data) % block_size)) % block_size
        padded_data = data + b"\x00" * padding_len

        encrypted = bytearray()
        for i in range(0, len(padded_data), block_size):
            block = padded_data[i : i + block_size]
            keystream = generate_keystream(key, block_size, seed=i // block_size)
            encrypted_block = bytes(a ^ b for a, b in zip(block, keystream))
            encrypted.extend(encrypted_block)

        return bytes(encrypted)
    except Exception as e:
        print(f"Error in xor_encrypt: {e}")
        return b""


def xor_decrypt(encrypted, key=ENCRYPTION_KEY_DUMMY, block_size=64):
    try:
        decrypted = bytearray()
        for i in range(0, len(encrypted), block_size):
            block = encrypted[i : i + block_size]
            keystream = generate_keystream(key, block_size, seed=i // block_size)
            decrypted_block = bytes(a ^ b for a, b in zip(block, keystream))
            decrypted.extend(decrypted_block)

        return bytes(decrypted).rstrip(b"\x00")
    except Exception as e:
        print(f"Error in xor_decrypt: {e}")
        return b""
