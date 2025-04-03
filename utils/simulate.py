import time
import random
import numpy as np
from scipy.stats import truncnorm
from utils.config import *

current_state = 0


def simulate_jitter(channel):
    try:
        # delay = np.random.normal(0, transmission_jitter)
        delay = (
            truncnorm.rvs(
                0,
                np.inf,
                loc=jitter_mu,
                scale=transmission_jitter_earth_moon,
            )
            if (channel == earth_moon)
            else truncnorm.rvs(
                0, np.inf, loc=jitter_mu, scale=transmission_jitter_moon_moon
            )
        )
        time.sleep(delay)

    except ValueError as e:
        print(f"[ERROR simulate_delay] Invalid parameter for Poisson distribution: {e}")
    except Exception as e:
        print(f"[ERROR simulate_delay] Unexpected error during delay simulation: {e}")


def base_simulate_delay(channel):
    try:
        delay = (
            transmission_delay_base_earth_moon
            if (channel == earth_moon)
            else transmission_delay_base_moon_moon
        )
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


def corrupt_packet(packet, block_size=1024, channel=earth_moon):
    global current_state
    try:

        transition_matrix = (
            transition_matrix_earth_moon
            if (channel == earth_moon)
            else transition_matrix_moon_moon
        )

        corruption_params = (
            corruption_params_earth_moon
            if (channel == earth_moon)
            else corruption_params_moon_moon
        )

        corrupted = bytearray(packet)

        for block_start in range(0, len(corrupted), block_size):
            block_end = min(block_start + block_size, len(corrupted))
            block = bytearray(corrupted[block_start:block_end])
            block_length = len(block)

            if current_state != 0:
                params = corruption_params[current_state]
                block_size_to_corrupt = round(
                    random.gauss(params["mean"], params["std"])
                )
                block_size_to_corrupt = max(0, min(block_size_to_corrupt, block_length))

                start_index = random.randint(0, block_length - block_size_to_corrupt)
                for i in range(start_index, start_index + block_size_to_corrupt):
                    block[i] = random.randint(0, 255)

            corrupted[block_start:block_end] = block
            probs = transition_matrix[current_state]
            current_state = int(np.random.choice(np.arange(6), p=probs))
        else:
            return bytes(corrupted)

    except IndexError as e:
        print(f"[ERROR corrupt_packet] Index out of range: {e}")
        return packet
    except TypeError as e:
        print(f"[ERROR corrupt_packet] Invalid data type: {e}")
        return packet
    except Exception as e:
        print(f"[ERROR corrupt_packet] Unexpected error: {e}")
        return packet


def simulate_channel(packet, channel):
    try:
        if (channel == earth_moon) and random.random() < EARTH_MOON_PACKET_LOSS_PROB:
            return None
        if (channel == moon_moon) and random.random() < MOON_MOON_PACKET_LOSS_PROB:
            return None

        base_simulate_delay(channel)
        simulate_jitter(channel)

        packet = corrupt_packet(packet, channel=channel)
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
        try:
            packet.accept()
        except:
            pass
