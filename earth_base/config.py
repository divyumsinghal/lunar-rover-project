from dotenv import load_dotenv
import os
from queue import Queue, PriorityQueue

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    verbose=True,
    override=False,
)
EARTH_BASE_IP = os.getenv("EARTH_BASE_IP")
LUNAR_ROVER_1_IP = os.getenv("LUNAR_ROVER_1_IP")

LUNAR_ROVER_SEND_DATA_PORT_1 = int(os.getenv("LUNAR_ROVER_SEND_DATA_PORT_1"))
LUNAR_ROVER_SEND_DATA_PORT_2 = int(os.getenv("LUNAR_ROVER_SEND_DATA_PORT_2"))
LUNAR_ROVER_SEND_DATA_PORT_3 = int(os.getenv("LUNAR_ROVER_SEND_DATA_PORT_3"))
LUNAR_ROVER_SEND_DATA_PORT_4 = int(os.getenv("LUNAR_ROVER_SEND_DATA_PORT_4"))

EARTH_BASE_SEND_CMD_PORT_1 = int(os.getenv("EARTH_BASE_SEND_CMD_PORT_1"))
EARTH_BASE_SEND_CMD_PORT_2 = int(os.getenv("EARTH_BASE_SEND_CMD_PORT_2"))
EARTH_BASE_SEND_CMD_PORT_3 = int(os.getenv("EARTH_BASE_SEND_CMD_PORT_3"))
EARTH_BASE_SEND_CMD_PORT_4 = int(os.getenv("EARTH_BASE_SEND_CMD_PORT_4"))

EARTH_RECEIVE_CMD_PORT_1 = int(os.getenv("LUNAR_ROVER_RECEIVE_CMD_PORT_1"))
EARTH_RECEIVE_CMD_PORT_2 = int(os.getenv("LUNAR_ROVER_RECEIVE_CMD_PORT_2"))
EARTH_RECEIVE_CMD_PORT_3 = int(os.getenv("LUNAR_ROVER_RECEIVE_CMD_PORT_3"))
EARTH_RECEIVE_CMD_PORT_4 = int(os.getenv("LUNAR_ROVER_RECEIVE_CMD_PORT_4"))

VIDEO_PORT = int(os.getenv("VIDEO_PORT"))
LUNAR_ROVER_RECIEVE_VIDEO_PORT = int(os.getenv("LUNAR_ROVER_RECIEVE_VIDEO_PORT"))

wait_time = 10
retries = 3
FRAME_RATE = 30

command_queue_1 = Queue()
command_queue_2 = Queue()
command_queue_3 = Queue()
command_queue_4 = Queue()

message_type = "Type"
message_data = "Data"
ack = "ACK"
cmd = "CMD"
video = "VID"
sens = "SENS"
temperature = "Temperature"
humidity = "Humidity"
handshake = "Handshake"

soil_moisture = "Soil Moisture"
soil_pH = "Soil pH"
soil_temp = "Soil Temperature"
soil_conductivity = "Soil Conductivity"

SECRET_KEY_EARTH_ROVER = os.getenv("SECRET_KEY_EARTH_ROVER").encode()
SECRET_KEY_ROVER_TUNNELLER = os.getenv("SECRET_KEY_ROVER_TUNNELLER").encode()
SECRET_KEY_ROVER_EXTERNAL = os.getenv("SECRET_KEY_ROVER_EXTERNAL").encode()

# Message type identifiers for packet filtering
MSG_TYPE_COMMAND = 1
MSG_TYPE_ACK = 2
MSG_TYPE_VIDEO = 3
MSG_TYPE_SENSOR = 4
MSG_TYPE_HANDSHAKE = 5

video_queue = Queue()
video_1 = "video_1"
video_2 = "video_2"
video_3 = "video_3"

play_frame_queue = PriorityQueue()
process_frame_queue = Queue()

video_to_store = {}

asked_for_video = False

earth_moon = "earth_moon"
moon_moon = "moon_moon"

EARTH_BASE_HANDSHAKE_PORT = int(os.getenv("EARTH_BASE_HANDSHAKE_PORT"))
LUNAR_ROVER_HANDSHAKE_PORT_EARTH = int(os.getenv("LUNAR_ROVER_HANDSHAKE_PORT_EARTH"))
LUNAR_ROVER_HANDSHAKE_PORT_TUNNELLER = int(
    os.getenv("LUNAR_ROVER_HANDSHAKE_PORT_TUNNELLER")
)
LUNAR_TUNNELLER_HANDSHAKE_PORT = int(os.getenv("LUNAR_TUNNELLER_HANDSHAKE_PORT"))

sensor_data_recv_queue = Queue()
connection_with_rover = False
immediately_check_connection_with_rover = False

handshake_interval = 100
handshake_timeout = 150
