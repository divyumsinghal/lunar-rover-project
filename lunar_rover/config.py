from dotenv import load_dotenv
import os
from queue import Queue

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    verbose=True,
    override=False,
)

EARTH_BASE_IP = os.getenv("EARTH_BASE_IP")
LUNAR_ROVER_1_IP = os.getenv("LUNAR_ROVER_1_IP")

EARTH_SEND_DATA_PORT_1 = int(os.getenv("EARTH_SEND_DATA_PORT_1"))
EARTH_SEND_DATA_PORT_2 = int(os.getenv("EARTH_SEND_DATA_PORT_2"))
EARTH_SEND_DATA_PORT_3 = int(os.getenv("EARTH_SEND_DATA_PORT_3"))
EARTH_SEND_DATA_PORT_4 = int(os.getenv("EARTH_SEND_DATA_PORT_4"))

EARTH_RECEIVE_CMD_PORT_1 = int(os.getenv("EARTH_RECEIVE_CMD_PORT_1"))
EARTH_RECEIVE_CMD_PORT_2 = int(os.getenv("EARTH_RECEIVE_CMD_PORT_2"))
EARTH_RECEIVE_CMD_PORT_3 = int(os.getenv("EARTH_RECEIVE_CMD_PORT_3"))
EARTH_RECEIVE_CMD_PORT_4 = int(os.getenv("EARTH_RECEIVE_CMD_PORT_4"))

EARTH_RECIEVE_VIDEO_PORT = int(os.getenv("EARTH_RECIEVE_VIDEO_PORT"))
VIDEO_PATH = os.path.join(os.path.dirname(__file__), "Video.mp4")
SEND_VIDEO_PORT = int(os.getenv("SEND_VIDEO_PORT"))
SECRET_KEY = os.getenv("SECRET_KEY").encode()

LUNAR_TUNNELLER_IP = os.getenv("LUNAR_TUNNELLER_IP")
LUNAR_TUNNELLER_RECV_CMD_PORT = int(os.getenv("LUNAR_TUNNELLER_RECV_CMD_PORT"))

TO_ROVER_TUNNELLER_SEND_DATA_PORT = int(os.getenv("TO_ROVER_TUNNELLER_SEND_DATA_PORT"))

ROVER_RECIEVE_VIDEO_PORT = int(os.getenv("ROVER_RECIEVE_VIDEO_PORT"))

wait_time = 10
retries = 3
nf_queue_run = 1

command_queue_1 = Queue()
command_queue_2 = Queue()
command_queue_3 = Queue()
command_queue_4 = Queue()

message_type = "Type"
message_data = "Data"
invalid_command = "Invalid Command"
ack = "ACK"
cmd = "CMD"
video = "VID"
sens = "SENS"
temperature = "Temperature"
humidity = "Humidity"


soil_moisture = "Soil Moisture"
soil_pH = "Soil pH"
soil_temp = "Soil Temperature"
soil_conductivity = "Soil Conductivity"

soil_moisture_sent = "Soil Moisture Sent    "
soil_pH_sent = "Soil pH Sent          "
soil_temp_sent = "Soil Temperature Sent "
soil_conductivity_sent = "Soil Conductivity Sent"


# Message type identifiers for packet filtering
MSG_TYPE_COMMAND = 1
MSG_TYPE_ACK = 2
MSG_TYPE_VIDEO = 3
MSG_TYPE_SENSOR = 4

video_queue = Queue()
video_1 = "video_1"
video_2 = "video_2"
video_3 = "video_3"


earth_moon = "earth_moon"
moon_moon = "moon_moon"


tunneller_command_queue = Queue()
asked_for_video = False
