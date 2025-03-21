import struct
import cv2
import numpy as np
import time
import socket
from src.config import *
from utils.client_server_comm import secure_receive
import src.config as config


def receive_video_from_rover(recv_socket):
    print(f"[EARTH - RECEIVE] Listening for video on port {VIDEO_PORT}")
    print(f"[DEBUG] Video receive socket: {recv_socket.getsockname()}")

    # Add a simple raw receive test
    print("[DEBUG] Testing raw packet receive before entering main loop...")
    try:
        # Set a shorter timeout for this test
        recv_socket.settimeout(5)
        test_data, addr = recv_socket.recvfrom(4096)
        print(f"[DEBUG] Received raw test packet: {test_data} from {addr}")
        # Reset timeout to None (blocking mode) for normal operation
        recv_socket.settimeout(None)
    except socket.timeout:
        print("[WARNING] No test packets received within timeout")
        recv_socket.settimeout(None)
    except Exception as e:
        print(f"[ERROR] Error during test receive: {e}")
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

    try:
        while True:
            try:
                # Receive the frame data with packet type filtering
                receipt_time = time.time()

                # First check if it's a raw direct message
                try:
                    recv_socket.settimeout(0.5)  # Brief timeout for checking
                    raw_data, addr = recv_socket.recvfrom(65536)

                    # Check if this might be a test packet
                    if raw_data.startswith(b"VIDEO_CONNECTION_TEST"):
                        print(f"[DEBUG] Received video test packet from {addr}")
                        continue

                    # Process through secure_receive to handle video frames
                    recv_socket.settimeout(None)
                    timestamp, frame_data, addr = secure_receive(
                        recv_socket, packet_type=MSG_TYPE_VIDEO
                    )
                except socket.timeout:
                    # No raw packets, try regular secure receive
                    recv_socket.settimeout(None)
                    timestamp, frame_data, addr = secure_receive(
                        recv_socket, packet_type=MSG_TYPE_VIDEO
                    )

                if timestamp is not None and frame_data is not None:
                    # Successfully received frame
                    frames_received += 1
                    process_time = time.time() - receipt_time

                    # Calculate timing data
                    if last_timestamp is not None:
                        time_diff = timestamp - last_timestamp
                        if time_diff < 0:
                            print(
                                f"[WARNING] Out of order frame detected: current={timestamp}, previous={last_timestamp}"
                            )

                    # Frame size information
                    frame_size = len(frame_data) if frame_data else 0

                    # Log every 30 frames to avoid console spam
                    if frames_received % 30 == 0:
                        print(
                            f"[DEBUG] Received frame {frames_received}: timestamp={timestamp}, size={frame_size} bytes, from={addr}"
                        )
                        print(
                            f"[DEBUG] Frame processing time: {process_time*1000:.2f}ms"
                        )

                        # Periodic statistics
                        current_time = time.time()
                        elapsed = current_time - last_report_time
                        if elapsed >= 5:  # Report every 5 seconds
                            fps = (
                                30 / elapsed
                            )  # Assuming we got 30 frames since last report
                            total_elapsed = current_time - start_time
                            avg_fps = frames_received / total_elapsed
                            print(f"[INFO] Receiving statistics:")
                            print(f"[INFO] - Frames received: {frames_received}")
                            print(f"[INFO] - Frames dropped: {frames_dropped}")
                            print(f"[INFO] - Current FPS: {fps:.2f}")
                            print(f"[INFO] - Average FPS: {avg_fps:.2f}")
                            print(f"[INFO] - Total time: {total_elapsed:.2f}s")
                            last_report_time = current_time

                    # Add to frame queue for playback
                    try:
                        frame_queue.put((int(timestamp), frame_data))
                        last_timestamp = timestamp
                    except Exception as e:
                        print(f"[ERROR] Failed to add frame to queue: {e}")
                        frames_dropped += 1
                else:
                    # Failed to receive frame
                    frames_dropped += 1
                    if frames_dropped % 10 == 0:  # Log every 10 dropped frames
                        print(f"[WARNING] Dropped {frames_dropped} frames so far")

            except Exception as e:
                print(f"[ERROR] Exception while receiving frame: {e}")
                import traceback

                traceback.print_exc()
                frames_dropped += 1
                # Brief pause to avoid CPU spinning on repeated errors
                time.sleep(0.1)

    except KeyboardInterrupt:
        # Clean shutdown on Ctrl+C
        print("[INFO] Video receiving stopped by user")
    except Exception as e:
        print(f"[ERROR] Fatal error in video receiving: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Final statistics
        total_time = time.time() - start_time
        print(f"[INFO] Video receiving summary:")
        print(f"[INFO] - Total frames received: {frames_received}")
        print(f"[INFO] - Total frames dropped: {frames_dropped}")
        print(
            f"[INFO] - Success rate: {frames_received/(frames_received+frames_dropped)*100:.1f}%"
        )
        print(f"[INFO] - Average FPS: {frames_received/total_time:.2f}")
        print(f"[INFO] - Total run time: {total_time:.2f}s")
