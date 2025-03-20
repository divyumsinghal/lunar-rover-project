import time
import random
import numpy as np

transmission_delay = 1400  # ms
transmission_min = 1.3
cosmic_ray_prob = 0.00001
num_bits_to_flip = 1


def simulate_delay():
    try:
        delay = np.random.poisson(lam=transmission_delay)
        delay = delay / 1000  # Convert to seconds
        if delay < transmission_min:
            delay = transmission_min
        time.sleep(delay)
    except ValueError as e:
        print(f"[ERROR simulate_delay] Invalid parameter for Poisson distribution: {e}")
    except Exception as e:
        print(f"[ERROR simulate_delay] Unexpected error during delay simulation: {e}")


def super_mario_speedrun_simulator(packet):
    try:
        new_data = bytearray(packet)

        if random.random() < cosmic_ray_prob:
            for _ in range(num_bits_to_flip):
                byte_index = random.randint(0, len(new_data) - 1)
                bit_index = random.randint(0, 7)
                # Flip the bit at the selected position using XOR.
                new_data[byte_index] ^= 1 << bit_index
        return bytes(new_data)

    except IndexError as e:
        print(f"[ERROR super_mario_speedrun_simulator] Index out of range: {e}")
        return packet
    except TypeError as e:
        print(f"[ERROR super_mario_speedrun_simulator] Invalid data type: {e}")
        return packet
    except Exception as e:
        print(f"[ERROR super_mario_speedrun_simulator] Unexpected error: {e}")
        return packet


def corrupt_packet(packet):
    try:
        if not packet:
            print("[ERROR corrupt_packet] Empty packet provided")
            return packet

        curropted_packet = bytearray(packet)
        length = len(curropted_packet)

        block_size = round(random.gauss(5.0, 3.0))
        block_size = max(1, block_size)
        block_size = min(
            block_size, length // 10 or 1
        )  # Ensure at least 1 if length < 10

        start_index = random.randint(0, length - block_size)

        for i in range(start_index, start_index + block_size):
            curropted_packet[i] = random.randint(0, 255)

        return bytearray(curropted_packet)

    except IndexError as e:
        print(f"[ERROR corrupt_packet] Index out of range: {e}")
        return packet
    except TypeError as e:
        print(f"[ERROR corrupt_packet] Invalid packet type: {e}")
        return packet
    except Exception as e:
        print(f"[ERROR corrupt_packet] Unexpected error during packet corruption: {e}")
        return packet


def simulate_channel(packet):
    try:
        if random.random() < 0.05:
            return None

        simulate_delay()

        packet = corrupt_packet(packet)
        packet = super_mario_speedrun_simulator(packet)

        return packet
    except Exception as e:
        print(
            f"[ERROR simulate_channel] Unexpected error during channel simulation: {e}"
        )
        return packet


def process_packet_in_the_channel(packet):
    try:
        payload = packet.get_payload()
        impaired_payload = simulate_channel(payload)
        if impaired_payload is None:
            packet.drop()
        else:
            packet.set_payload(impaired_payload)
            packet.accept()
    except AttributeError as e:
        print(f"[ERROR process_packet_in_the_channel] Invalid packet object: {e}")
    except Exception as e:
        print(
            f"[ERROR process_packet_in_the_channel] Unexpected error during packet processing: {e}"
        )
        # In case of error, try to accept the packet anyway as a fallback
        try:
            packet.accept()
        except:
            pass
