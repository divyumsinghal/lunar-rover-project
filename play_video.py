import cv2


def play_video(video_path):
    # Create a VideoCapture object
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Video resolution: {frame_width}x{frame_height}, FPS: {fps}")

    # Create a window
    window_name = "Video Player"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Set window size
    cv2.resizeWindow(window_name, frame_width, frame_height)

    while True:
        # Read a frame
        ret, frame = cap.read()

        # If frame is read correctly ret is True
        if not ret:
            print("End of video or error reading frame.")
            break

        # Display the frame
        cv2.imshow(window_name, frame)

        # Wait for a key press, and make playback speed match video FPS
        # 1000/fps gives us the wait time in milliseconds between frames
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord("q"):
            print("Playback stopped by user.")
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Replace with your video file path
    video_file = "output1.mp4"
    play_video(video_file)
