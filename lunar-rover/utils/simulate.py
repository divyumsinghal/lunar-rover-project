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


'''
def simulate_delay():
    """
    Simulate the transmission delay (in milliseconds) for a packet using a six-state
    Markov chain. The states represent different network conditions:

      0: Minimal delay (e.g., excellent conditions)
      1: Very good delay
      2: Good delay
      3: Regular delay
      4: Bad delay
      5: Very bad delay (rare state with high delay and jitter)

    This function uses an internal static variable to remember the current state across calls.
    It draws the delay from a normal distribution based on the current state's parameters,
    ensuring a non-negative delay, and then updates the state using the defined transition matrix.

    Returns:
        float: The simulated delay in milliseconds.
    """
    # Define the six states.
    states = list(range(6))

    # Transition matrix: rows are current state, columns are next state.
    # Probabilities are set so that extreme delays (state 5) remain rare.
    transition_matrix = np.array(
        [
            [0.80, 0.10, 0.05, 0.03, 0.01, 0.01],  # from state 0: Minimal delay
            [0.05, 0.70, 0.15, 0.05, 0.03, 0.02],  # from state 1: Very good delay
            [0.02, 0.10, 0.70, 0.10, 0.05, 0.03],  # from state 2: Good delay
            [0.01, 0.03, 0.10, 0.70, 0.10, 0.06],  # from state 3: Regular delay
            [0.005, 0.01, 0.04, 0.10, 0.70, 0.145],  # from state 4: Bad delay
            [0.005, 0.005, 0.005, 0.02, 0.05, 0.915],  # from state 5: Very bad delay
        ]
    )

    # Delay parameters (mean delay, standard deviation) in milliseconds for each state.
    delay_params = {
        0: (1.3, 10),  # Minimal delay
        1: (1.4, 15),  # Very good delay
        2: (1.5, 20),  # Good delay
        3: (2, 30),  # Regular delay
        4: (7, 50),  # Bad delay
        5: (10, 80),  # Very bad delay
    }

    # Initialize the current state if not already set.
    if not hasattr(simulate_delay, "current_state"):
        simulate_delay.current_state = 0  # start with minimal delay

    current_state = simulate_delay.current_state

    # Draw the delay from a normal distribution based on the current state's parameters.
    mean, std = delay_params[current_state]
    delay = max(0, random.gauss(mean, std))  # ensure non-negative delay

    # Update the state using the transition matrix.
    probs = transition_matrix[current_state]
    new_state = int(np.random.choice(states, p=probs))
    simulate_delay.current_state = new_state

    time.sleep(delay)
'''


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


'''
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

def corrupt_packet(packet, drop_on_error=False, block_size=100):
    """
    Simulate packet corruption using a three-state Gilbert–Elliott model that corrupts
    contiguous blocks of bytes rather than individual bits.

    The channel is modeled as a Markov chain with three states:
      - "very_good": almost no corruption (mean corruption block size is very low)
      - "regular": moderate corruption (typical burst size)
      - "very_bad": severe corruption (large burst of errors, but rarely entered)

    For each block of the packet, a block corruption length is drawn from a Gaussian
    distribution (with parameters depending on the current state) and then that many
    contiguous bytes (starting at a random index in the block) are overwritten with
    random values.

    After processing each block, the state is updated using the Markov transition matrix,
    allowing transitions into any state. This captures bursty error behavior over the packet.

    Parameters:
        packet (bytes): The original packet as a bytes object.
        drop_on_error (bool): If True, any error in any block results in the packet being dropped (None returned).
        block_size (int): The size (in bytes) of each block to process.

    Returns:
        bytes or None: The corrupted packet as a bytes object, or None if drop_on_error is True and any corruption occurred.
    """
    # Define the three states
    states = ["very_good", "regular", "very_bad"]

    # Transition matrix: from current state (row) to next state (column)
    # Probabilities are chosen so that "very_bad" is rarely entered from a "very_good" state.
    transition_matrix = {
        "very_good": {"very_good": 0.90, "regular": 0.09, "very_bad": 0.01},
        "regular": {"very_good": 0.20, "regular": 0.70, "very_bad": 0.10},
        "very_bad": {"very_good": 0.30, "regular": 0.40, "very_bad": 0.30},
    }

    # Corruption parameters (mean and standard deviation for block corruption size)
    # Adjust these values to reflect different error burst characteristics:
    corruption_params = {
        "very_good": {"mean": 0, "std": 0.5},  # minimal corruption
        "regular": {"mean": 1, "std": 1},  # moderate burst errors
        "very_bad": {"mean": 5, "std": 3},  # severe burst errors
    }

    # Convert packet to a mutable bytearray.
    corrupted = bytearray(packet)
    error_occurred = False

    # Start in the "very_good" state.
    current_state = "very_good"

    # Process the packet in blocks.
    for block_start in range(0, len(corrupted), block_size):
        block_end = min(block_start + block_size, len(corrupted))
        block = bytearray(corrupted[block_start:block_end])
        block_length = len(block)

        # Determine how many bytes to corrupt in this block based on the current state.
        params = corruption_params[current_state]
        block_size_to_corrupt = round(random.gauss(params["mean"], params["std"]))
        # Clamp corruption size to be at least 0 and at most the block length.
        block_size_to_corrupt = max(0, min(block_size_to_corrupt, block_length))

        if block_size_to_corrupt > 0:
            # Choose a random starting index such that the corruption block fits within the current block.
            start_index = random.randint(0, block_length - block_size_to_corrupt)
            for i in range(start_index, start_index + block_size_to_corrupt):
                block[i] = random.randint(0, 255)
            error_occurred = True

        # Write the (possibly) corrupted block back into the overall packet.
        corrupted[block_start:block_end] = block

        # Update the channel state using the transition probabilities.
        probs = list(transition_matrix[current_state].values())
        next_state = random.choices(
            list(transition_matrix[current_state].keys()), weights=probs, k=1
        )[0]
        current_state = next_state

    if drop_on_error and error_occurred:
        return None
    else:
        return bytes(corrupted)
'''


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
            [0.95, 0.04, 0.005, 0.005, 0.0, 0.0],  # from state 0 (no corruption)
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

        # simulate_delay()

        # base_simulate_delay()
        # simulate_jitter()

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
