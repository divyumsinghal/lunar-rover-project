import time
import cv2
import os
from src.config import *
from utils.client_server_comm import secure_send


def send_video_to_earth(send_socket):
    print(
        f"[EARTH COMM - SEND] Sending video data to Earth on port {EARTH_RECIEVE_VIDEO_PORT}"
    )
    print(f"[DEBUG] Video socket local endpoint: {send_socket.getsockname()}")
    print(f"[DEBUG] Earth BASE IP: {EARTH_BASE_IP}")
    print(f"[DEBUG] Earth RECEIVE VIDEO PORT: {EARTH_RECIEVE_VIDEO_PORT}")
    print(f"[DEBUG] Destination: {EARTH_BASE_IP}:{EARTH_RECIEVE_VIDEO_PORT}")

    while True:
        if not video_queue.empty():
            try:
                command = video_queue.get()
                print(f"[INFO] Video command received: '{command}'")
                if command != video_1:
                    print(f"[ERROR] Unrecognized video command: '{command}'")
                    continue

                print(f"[INFO] Starting video transmission for command: {command}")

                if not os.path.exists(VIDEO_PATH):
                    print(f"[ERROR] Video file not found at path: {VIDEO_PATH}")
                    continue

                print(f"[DEBUG] Opening video file: {VIDEO_PATH}")
                cap = cv2.VideoCapture(VIDEO_PATH)
                if not cap.isOpened():
                    print(
                        "[ERROR] Failed to open video file. Check format compatibility."
                    )
                    continue

                # Get video properties for debugging
                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                frame_rate = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                print(
                    f"[DEBUG] Video properties: {frame_width}x{frame_height}, {frame_rate:.2f} FPS, {frame_count} frames"
                )
                if frame_rate > 0:
                    print(
                        f"[DEBUG] Estimated video duration: {frame_count/frame_rate:.2f} seconds"
                    )
                else:
                    print("[WARNING] Frame rate is zero or undefined.")

                frames_sent = 0
                frames_failed = 0
                start_time = time.time()

                frame_idx = 0
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        print(f"[INFO] End of video stream after {frames_sent} frames")
                        break

                    frame_idx += 1
                    frame_start = time.time()
                    if frame_idx % 30 == 0:
                        print(f"[DEBUG] Processing frame {frame_idx}/{frame_count}")

                    # (Optional) Resize the frame if you need to reduce the data size:
                    # frame = cv2.resize(frame, (640, 480))

                    # Encode frame as JPEG
                    encode_start = time.time()
                    ret, buffer = cv2.imencode(
                        ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70]
                    )
                    if not ret:
                        print(f"[ERROR] Failed to encode frame {frame_idx}")
                        frames_failed += 1
                        continue

                    encode_time = time.time() - encode_start
                    frame_data = buffer.tobytes()
                    frame_size = len(frame_data)
                    if frame_idx % 30 == 0:
                        print(
                            f"[DEBUG] Frame {frame_idx} encoded: {frame_size} bytes, encoding took {encode_time*1000:.2f}ms"
                        )

                    # Send a test packet (if desired, you might choose to send this less frequently)
                    destination = (EARTH_BASE_IP, EARTH_RECIEVE_VIDEO_PORT)
                    # Send the frame with secure_send (using frames_sent as a sequence number)
                    try:
                        secure_send(
                            frames_sent,
                            send_socket,
                            frame_data,
                            destination,
                            packet_type=MSG_TYPE_VIDEO,
                        )
                        frames_sent += 1
                    except Exception as e:
                        print(f"[ERROR] Failed to send frame {frame_idx}: {e}")
                        frames_failed += 1

                    send_time = time.time() - frame_start
                    if frame_idx % 30 == 0:
                        print(
                            f"[DEBUG] Frame {frame_idx} sent in {send_time*1000:.2f}ms"
                        )

                    # Sleep to match the original frame rate if possible
                    if frame_rate > 0:
                        expected_frame_time = 1.0 / frame_rate
                        processing_time = time.time() - frame_start
                        if processing_time < expected_frame_time:
                            time.sleep(expected_frame_time - processing_time)

                total_time = time.time() - start_time
                print(f"[INFO] Video transmission complete:")
                if frame_count > 0:
                    print(
                        f"[INFO] - Frames sent: {frames_sent}/{frame_count} ({frames_sent/frame_count*100:.1f}%)"
                    )
                print(f"[INFO] - Frames failed: {frames_failed}")
                print(f"[INFO] - Total time: {total_time:.2f} seconds")
                if total_time > 0:
                    print(
                        f"[INFO] - Effective frame rate: {frames_sent/total_time:.2f} FPS"
                    )
                cap.release()
                print("[INFO] Video file closed")
            except Exception as e:
                print(f"[ERROR] Failed to process video command: {e}")
                import traceback

                traceback.print_exc()
        else:
            time.sleep(0.1)  # Avoid busy waiting
