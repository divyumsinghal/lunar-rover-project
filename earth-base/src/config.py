from dotenv import load_dotenv
import os
from queue import Queue

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    verbose=True,
    override=False,
)

LUNAR_ROVER_1_IP = os.getenv("LUNAR_ROVER_1_IP")
LOCAL_IP = os.getenv("LOCAL_IP")

LUNAR_ROVER_SEND_DATA_PORT = int(os.getenv("LUNAR_ROVER_SEND_DATA_PORT"))
EARTH_RECEIVE_CMD_PORT = int(os.getenv("LUNAR_ROVER_RECEIVE_CMD_PORT"))
VIDEO_PORT = int(os.getenv("VIDEO_PORT"))
EARTH_BASE_SEND_CMD_PORT = int(os.getenv("EARTH_BASE_SEND_CMD_PORT"))
LUNAR_ROVER_RECIEVE_VIDEO_PORT = int(os.getenv("LUNAR_ROVER_RECIEVE_VIDEO_PORT"))

wait_time = 10
retries = 3
nf_queue_run = 1

command_queue = Queue()
message_type = "Type"
message_data = "Data"
ack = "ACK"
cmd = "CMD"
video = "VID"
sens = "SENS"
temperature = "Temperature"


video_queue = Queue()
video_1 = "video_1"
video_2 = "video_2"
video_3 = "video_3"
