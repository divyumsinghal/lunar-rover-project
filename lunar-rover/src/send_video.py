import time
import cv2
import os
from src.config import *
from utils.client_server_comm import secure_send, secure_receive


def send_video_to_earth(send_socket):
    print(
        f"[EARTH COMM - SEND] Sending video data to Earth on port {EARTH_RECIEVE_VIDEO_PORT}"
    )
    print(f"[DEBUG] Video socket local endpoint: {send_socket.getsockname()}")
    print(f"[DEBUG] Earth BASE IP: {EARTH_BASE_IP}")
    print(f"[DEBUG] Earth RECEIVE VIDEO PORT: {EARTH_RECIEVE_VIDEO_PORT}")

    print("[DEBUG] Video socket details:")
    print(f"[DEBUG] - Local socket: {send_socket.getsockname()}")
    print(f"[DEBUG] - Destination: {EARTH_BASE_IP}:{EARTH_RECIEVE_VIDEO_PORT}")

    while True:
        if not video_queue.empty():
            try:
                command = video_queue.get()
                print(f"[INFO] Video command received: '{command}'")

                if command == video_1:
                    print(f"[INFO] Starting video transmission for command: {command}")

                    # Check if video file exists
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
                        f"[DEBUG] Video properties: {frame_width}x{frame_height}, {frame_rate} FPS, {frame_count} frames"
                    )
                    print(
                        f"[DEBUG] Estimated video duration: {frame_count/frame_rate:.2f} seconds"
                    )

                    frames_sent = 0
                    frames_failed = 0
                    start_time = time.time()

                    while cap.isOpened():
                        try:
                            for i in range(frame_count):
                                frame_start = time.time()
                                ret, frame = cap.read()
                                if not ret:
                                    print(
                                        f"[INFO] End of video stream after {frames_sent} frames"
                                    )
                                    break

                                # Debug frame info
                                if i % 30 == 0:  # Log every 30 frames
                                    print(
                                        f"[DEBUG] Processing frame {i+1}/{frame_count}"
                                    )

                                # Resize frame to reduce data size if needed
                                # frame = cv2.resize(frame, (640, 480))

                                # Encode the frame as JPEG to compress data
                                encode_start = time.time()
                                ret, buffer = cv2.imencode(
                                    ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70]
                                )
                                if not ret:
                                    print(f"[ERROR] Failed to encode frame {i+1}")
                                    frames_failed += 1
                                    continue

                                encode_time = time.time() - encode_start
                                frame_data = buffer.tobytes()
                                frame_size = len(frame_data)

                                if i % 30 == 0:  # Log every 30 frames
                                    print(
                                        f"[DEBUG] Frame {i+1} encoded: {frame_size} bytes, encoding took {encode_time*1000:.2f}ms"
                                    )

                                # Use current time in milliseconds as timestamp
                                # timestamp = int(time.time() * 1000)

                                # Send the frame
                                send_start = time.time()
                                try:
                                    destination = (
                                        EARTH_BASE_IP,
                                        EARTH_RECIEVE_VIDEO_PORT,
                                    )
                                    print(
                                        f"[DEBUG] Sending frame {i+1} to {destination}, size: {frame_size} bytes"
                                    )

                                    # Send a test packet to verify connectivity
                                    try:
                                        test_message = b"VIDEO_CONNECTION_TEST"
                                        send_socket.sendto(
                                            test_message,
                                            (EARTH_BASE_IP, EARTH_RECIEVE_VIDEO_PORT),
                                        )
                                        print(
                                            f"[DEBUG] Sent test packet to Earth Base at {EARTH_BASE_IP}:{EARTH_RECIEVE_VIDEO_PORT}"
                                        )
                                    except Exception as e:
                                        print(
                                            f"[ERROR] Failed to send test packet: {e}"
                                        )

                                    secure_send(
                                        frames_sent,
                                        send_socket,
                                        frame_data,
                                        destination,
                                        packet_type=MSG_TYPE_VIDEO,  # Specify that this is a video packet
                                    )
                                    frames_sent += 1

                                    # Calculate and respect frame rate for smoother streaming
                                    send_time = time.time() - send_start
                                    frame_time = time.time() - frame_start

                                    if i % 30 == 0:  # Log every 30 frames
                                        print(
                                            f"[DEBUG] Frame {i+1} sent in {send_time*1000:.2f}ms, total processing: {frame_time*1000:.2f}ms"
                                        )

                                except Exception as e:
                                    print(f"[ERROR] Failed to send frame {i+1}: {e}")
                                    frames_failed += 1

                            # End of video statistics
                            total_time = time.time() - start_time
                            print(f"[INFO] Video transmission complete:")
                            print(
                                f"[INFO] - Frames sent: {frames_sent}/{frame_count} ({frames_sent/frame_count*100:.1f}%)"
                            )
                            print(f"[INFO] - Frames failed: {frames_failed}")
                            print(f"[INFO] - Total time: {total_time:.2f} seconds")
                            print(
                                f"[INFO] - Effective frame rate: {frames_sent/total_time:.2f} FPS"
                            )
                            break  # Exit the while cap.isOpened() loop

                        except Exception as e:
                            print(f"[ERROR] Exception during frame processing: {e}")
                            import traceback

                            traceback.print_exc()

                    cap.release()
                    print("[INFO] Video file closed")
                else:
                    print(f"[ERROR] Unrecognized video command: '{command}'")
            except Exception as e:
                print(f"[ERROR] Failed to process video command: {e}")
                import traceback

                traceback.print_exc()
