from src.config import *
import cv2
import numpy as np
import queue
import time


def video_playback():
    """
    Waits until the first frame is received,
    then waits an additional 10 seconds before starting playback.
    Continuously retrieves frames from the queue and displays them.
    """
    print("[INFO] Video playback module initialized")
    print(f"[DEBUG] Target frame rate: {FRAME_RATE} FPS")
    print("[INFO] Waiting for first frame...")

    # Wait until at least one frame is received
    first_frame_received = False
    wait_start = time.time()

    while not first_frame_received:
        if not frame_queue.empty():
            first_frame_received = True
            first_timestamp, _ = frame_queue.queue[0]
            print(
                f"[INFO] First frame received (timestamp: {first_timestamp}) after {time.time() - wait_start:.2f}s"
            )
            break

        # Timeout if waiting too long
        if time.time() - wait_start > 60:  # 1 minute timeout
            print("[WARNING] Waited 60 seconds for first frame, continuing anyway...")
            break

        time.sleep(0.5)

    if not first_frame_received:
        print("[WARNING] No frames received, but continuing with playback loop...")
    else:
        buffer_time = 10  # seconds to buffer
        print(f"[INFO] Buffering video for {buffer_time} seconds...")
        time.sleep(buffer_time)
        buffered_frames = frame_queue.qsize()
        print(f"[INFO] Buffered {buffered_frames} frames, starting playback")

    # Playback statistics
    frames_displayed = 0
    frames_dropped = 0
    start_time = time.time()
    last_report_time = start_time
    last_frame_time = start_time
    frame_times = []  # To track frame timing for FPS calculation

    # Create window with a specific size
    cv2.namedWindow("Video Playback", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video Playback", 1280, 720)

    try:
        while True:
            try:
                frame_start = time.time()

                # Report queue status periodically
                current_time = time.time()
                if current_time - last_report_time >= 5:  # Every 5 seconds
                    queue_size = frame_queue.qsize()
                    elapsed = current_time - start_time
                    avg_fps = frames_displayed / elapsed if elapsed > 0 else 0

                    # Calculate recent FPS using the last 30 frame times
                    if len(frame_times) > 0:
                        recent_fps = len(frame_times) / sum(frame_times)
                    else:
                        recent_fps = 0

                    # Reset for next period
                    last_report_time = current_time
                    frame_times = []

                # Get the next frame (ordered by timestamp)
                timestamp, frame_data = frame_queue.get(timeout=1)

                # Track time between frames
                frame_interval = time.time() - last_frame_time
                if len(frame_times) >= 30:
                    frame_times.pop(0)  # Keep only the last 30 frame times
                frame_times.append(frame_interval)
                last_frame_time = time.time()

                if frames_displayed % 30 == 0:  # Log every 30 frames
                    print(
                        f"[DEBUG] Playing frame with timestamp {timestamp}, queue size: {frame_queue.qsize()}"
                    )

                # Convert frame_data back into an image using OpenCV
                decode_start = time.time()
                np_arr = np.frombuffer(frame_data, dtype=np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                decode_time = time.time() - decode_start

                if frame is None:
                    print(f"[ERROR] Failed to decode frame at timestamp {timestamp}")
                    frames_dropped += 1
                    continue

                # Display the frame
                display_start = time.time()
                cv2.imshow("Video Playback", frame)
                display_time = time.time() - display_start

                if frames_displayed % 30 == 0:  # Log timing details periodically
                    frame_time = time.time() - frame_start
                    print(
                        f"[DEBUG] Frame timing: decode={decode_time*1000:.1f}ms, display={display_time*1000:.1f}ms, total={frame_time*1000:.1f}ms"
                    )

                frames_displayed += 1

                # Wait for a short time (approx 1/FRAME_RATE seconds)
                # Use remaining time to maintain consistent frame rate
                elapsed = time.time() - frame_start
                wait_time = max(1, int((1000 / FRAME_RATE) - elapsed * 1000))

                if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                    print("[INFO] Playback stopped by user (q key)")
                    break

            except queue.Empty:
                # No frame available, wait a bit and try again
                time.sleep(0.01)

            except Exception as e:
                print(f"[ERROR] Playback exception: {e}")
                import traceback

                traceback.print_exc()
                frames_dropped += 1
                # Brief pause to avoid CPU spinning on repeated errors
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("[INFO] Playback stopped by keyboard interrupt")
    except Exception as e:
        print(f"[ERROR] Fatal playback error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Final summary statistics
        total_time = time.time() - start_time
        cv2.destroyAllWindows()
        print(f"[INFO] Playback summary:")
        print(f"[INFO] - Total frames displayed: {frames_displayed}")
        print(f"[INFO] - Total frames dropped: {frames_dropped}")
        print(f"[INFO] - Playback duration: {total_time:.2f}s")
        print(
            f"[INFO] - Average FPS: {frames_displayed/total_time if total_time > 0 else 0:.2f}"
        )
