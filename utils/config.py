import numpy as np

wait_time = 10
retries = 3
nf_queue_run = 1

message_type = "Type"
message_data = "Data"
ack = "ACK"
cmd = "CMD"
video = "VID"
sens = "SENS"
temperature = "Temperature"

# Message type identifiers for packet filtering
MSG_TYPE_COMMAND = 1
MSG_TYPE_ACK = 2
MSG_TYPE_VIDEO = 3
MSG_TYPE_SENSOR = 4
MSG_TYPE_HANDSHAKE = 5

video_1 = "video_1"
video_2 = "video_2"
video_3 = "video_3"


transmission_delay = 1800  # ms
transmission_delay_base_earth_moon = 1.7
transmission_delay_base_moon_moon = 0.1
jitter_mu = 0
transmission_jitter_earth_moon = 0.8
transmission_jitter_moon_moon = 0.05
cosmic_ray_prob = 0.00001
num_bits_to_flip = 1


transition_matrix_earth_moon = np.array(
    [
        [0.992, 0.005, 0.002, 0.001, 0.0, 0.0],  # from state 0 (no corruption)
        [0.80, 0.10, 0.08, 0.02, 0.0, 0.0],  # from state 1 (very good)
        [0.50, 0.10, 0.30, 0.05, 0.05, 0.0],  # from state 2 (good)
        [0.20, 0.15, 0.15, 0.30, 0.15, 0.05],  # from state 3 (regular)
        [0.20, 0.02, 0.07, 0.20, 0.41, 0.10],  # from state 4 (bad)
        [0.10, 0.05, 0.10, 0.20, 0.30, 0.25],  # from state 5 (very bad)
    ]
)

transition_matrix_moon_moon = np.array(
    [
        [0.995, 0.003, 0.001, 0.001, 0.0, 0.0],  # from state 0 (no corruption)
        [0.85, 0.12, 0.03, 0.0, 0.0, 0.0],  # from state 1 (very good)
        [0.05, 0.3, 0.6, 0.05, 0.0, 0.0],  # from state 2 (good)
        [0.05, 0.1, 0.3, 0.5, 0.05, 0.0],  # from state 3 (regular)
        [0.05, 0.01, 0.04, 0.3, 0.5, 0.1],  # from state 4 (bad)
        [0.02, 0.01, 0.02, 0.15, 0.4, 0.4],  # from state 5 (very bad)
    ]
)


corruption_params_earth_moon = {
    0: {"mean": 0, "std": 0},  # No corruption
    1: {"mean": 1, "std": 0.5},  # Very good: almost no corruption
    2: {"mean": 2, "std": 1},  # Good: low-level corruption
    3: {"mean": 3, "std": 2},  # Regular: moderate corruption
    4: {"mean": 5, "std": 3},  # Bad: severe corruption
    5: {"mean": 12, "std": 3},  # Very bad: extensive corruption
}

corruption_params_moon_moon = {
    0: {"mean": 0, "std": 0},  # No corruption
    1: {"mean": 1, "std": 0.5},  # Very good: almost no corruption
    2: {"mean": 2, "std": 1},  # Good: low-level corruption
    3: {"mean": 3, "std": 2},  # Regular: moderate corruption
    4: {"mean": 5, "std": 3},  # Bad: severe corruption
    5: {"mean": 12, "std": 3},  # Very bad: extensive corruption
}


earth_moon = "earth_moon"
moon_moon = "moon_moon"

EARTH_MOON_PACKET_LOSS_PROB = 0.05
MOON_MOON_PACKET_LOSS_PROB = 0.01

SECRET_KEY_DUMMY = b"SUPER_SECRET_ROVER_KEY_1"
ENCRYPTION_KEY_DUMMY = b"SUPER_SECRET_ROVER_KEY_ENCRYPTION_1"
