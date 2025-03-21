import time
import socket
import cv2
from src.config import *
from utils.client_server_comm import secure_receive
import src.config as config


def receive_video_from_rover(recv_socket):
    print(f"[EARTH - RECEIVE] Listening for video on port {VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {recv_socket.getsockname()}")

    recv_socket.settimeout(None)

    print("[INFO] Waiting for video request to be sent to rover...")
    while not config.asked_for_video:
        time.sleep(0.5)

    print("[INFO] Video request has been sent to rover, starting to receive frames")

    frames_received = 0
    frames_dropped = 0
    last_timestamp = None
    start_time = time.time()
    last_report_time = start_time
    last_frames_count = 0

    try:
        while True:
            receipt_time = time.time()
            try:
                # Always receive video frames via secure_receive
                timestamp, frame_data, addr = secure_receive(
                    recv_socket, packet_type=MSG_TYPE_VIDEO
                )
            except Exception as e:
                print(f"[ERROR] Exception in secure_receive: {e}")
                frames_dropped += 1
                time.sleep(0.1)
                continue

            if timestamp is not None and frame_data is not None:
                frames_received += 1

                if last_timestamp is not None and timestamp < last_timestamp:
                    print(
                        f"[WARNING] Out of order frame detected: current={timestamp}, previous={last_timestamp}"
                    )

                frame_size = len(frame_data)
                if frames_received % 30 == 0:
                    print(
                        f"[DEBUG] Received frame {frames_received}: timestamp={timestamp}, size={frame_size} bytes, from={addr}"
                    )

                # Add the frame to the playback queue
                try:
                    frame_queue.put((int(timestamp), frame_data))
                    last_timestamp = timestamp
                except Exception as e:
                    print(f"[ERROR] Failed to add frame to queue: {e}")
                    frames_dropped += 1
            else:
                frames_dropped += 1
                if frames_dropped % 10 == 0:
                    print(f"[WARNING] Dropped {frames_dropped} frames so far")
    except KeyboardInterrupt:
        print("[INFO] Video receiving stopped by user")
    except Exception as e:
        print(f"[ERROR] Fatal error in video receiving: {e}")
        import traceback

        traceback.print_exc()
    finally:
        total_time = time.time() - start_time
        print(f"[INFO] Video receiving summary:")
        print(f"[INFO] - Total frames received: {frames_received}")
        print(f"[INFO] - Total frames dropped: {frames_dropped}")
        total_frames = frames_received + frames_dropped
        if total_frames > 0:
            print(f"[INFO] - Success rate: {frames_received/total_frames*100:.1f}%")
        if total_time > 0:
            print(f"[INFO] - Average FPS: {frames_received/total_time:.2f}")
        print(f"[INFO] - Total run time: {total_time:.2f}s")
