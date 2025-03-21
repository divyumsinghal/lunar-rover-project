import time
import random
import numpy as np
from scipy.stats import truncnorm

transmission_delay = 1400  # ms
transmission_delay_base = 1.3
jitter_mu = 0
transmission_jitter = 0.1
cosmic_ray_prob = 0.00001
num_bits_to_flip = 1


def simulate_jitter():
    try:
        # delay = np.random.normal(0, transmission_jitter)
        delay = truncnorm.rvs(0, np.inf, loc=jitter_mu, scale=transmission_jitter)
        time.sleep(delay)
    except ValueError as e:
        print(f"[ERROR simulate_delay] Invalid parameter for Poisson distribution: {e}")
    except Exception as e:
        print(f"[ERROR simulate_delay] Unexpected error during delay simulation: {e}")


def base_simulate_delay():
    try:
        delay = transmission_delay_base
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


def corrupt_packet(packet, block_size=64):
    """
    Simulate packet corruption using a six-state Markov chain model.

    States:
      0 - Zero corruption (no corruption)
      1 - Very good (minimal corruption)
      2 - Good (low-level corruption)
      3 - Regular (moderate corruption)
      4 - Bad (severe corruption)
      5 - Very bad (extensive corruption, rare)

    The packet is processed in blocks of size 'block_size'. For each block,
    a corruption block size is drawn from a Gaussian distribution based on the
    current state's parameters. A contiguous block of bytes (of that size)
    within the block is then overwritten with random bytes.

    Parameters:
        packet (bytes): The original packet as a bytes object.
        drop_on_error (bool): If True, any error causes the packet to be dropped (None returned).
        block_size (int): The size of each block to process in bytes.

    Returns:
        bytes or None: The corrupted packet, or None if drop_on_error is True and any corruption occurred.
    """
    # Define states as integers: 0, 1, 2, 3, 4, 5.
    # Define a transition matrix (6x6) for the Markov chain.
    # Rows: current state, Columns: next state.
    # The probabilities here are chosen to keep state 5 rare and to model realistic transitions.
    transition_matrix = np.array(
        [
            [0.65, 0.24, 0.105, 0.005, 0.0, 0.0],  # from state 0 (no corruption)
            [0.10, 0.80, 0.08, 0.02, 0.0, 0.0],  # from state 1 (very good)
            [0.05, 0.10, 0.70, 0.10, 0.05, 0.0],  # from state 2 (good)
            [0.02, 0.05, 0.15, 0.60, 0.15, 0.03],  # from state 3 (regular)
            [0.01, 0.02, 0.07, 0.20, 0.60, 0.10],  # from state 4 (bad)
            [0.05, 0.05, 0.10, 0.20, 0.30, 0.30],  # from state 5 (very bad)
        ]
    )

    # Define corruption parameters for states 1 through 5.
    # State 0 implies no corruption so it is handled separately.
    # Each entry gives (mean, std) for the block corruption size.
    corruption_params = {
        0: {"mean": 0, "std": 0},  # No corruption
        1: {"mean": 1, "std": 0.5},  # Very good: almost no corruption
        2: {"mean": 2, "std": 1},  # Good: low-level corruption
        3: {"mean": 3, "std": 2},  # Regular: moderate corruption
        4: {"mean": 5, "std": 3},  # Bad: severe corruption
        5: {"mean": 12, "std": 3},  # Very bad: extensive corruption
    }

    # Convert the immutable packet bytes to a mutable bytearray.
    corrupted = bytearray(packet)
    error_occurred = False

    # Start in state 0 (no corruption).
    current_state = 0

    # Process the packet in blocks.
    for block_start in range(0, len(corrupted), block_size):
        block_end = min(block_start + block_size, len(corrupted))
        block = bytearray(corrupted[block_start:block_end])
        block_length = len(block)

        # If the current state is 0 (no corruption), skip corruption.
        if current_state != 0:
            params = corruption_params[current_state]
            # Sample the number of bytes to corrupt using a Gaussian distribution.
            block_size_to_corrupt = round(random.gauss(params["mean"], params["std"]))
            # Clamp to be at least 1 and at most the block length.
            block_size_to_corrupt = max(1, min(block_size_to_corrupt, block_length))

            # Choose a random starting index such that the corruption block fits.
            start_index = random.randint(0, block_length - block_size_to_corrupt)
            for i in range(start_index, start_index + block_size_to_corrupt):
                block[i] = random.randint(0, 255)
            error_occurred = True

        # Write the (possibly) corrupted block back into the packet.
        corrupted[block_start:block_end] = block

        # Update the channel state using the transition matrix.
        # Get the transition probabilities for the current state.
        probs = transition_matrix[current_state]
        # Choose the next state using the probabilities.
        current_state = int(np.random.choice(np.arange(6), p=probs))
    else:
        return bytes(corrupted)


def simulate_channel(packet):
    try:
        if random.random() < 0.05:
            return None

        base_simulate_delay()
        simulate_jitter()

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
