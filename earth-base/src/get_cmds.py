import tkinter as tk
import queue
import threading
import time
from src.config import *


def start_gui(command_queue, video_queue):
    root = tk.Tk()
    root.title("Earth Base - Command Input")

    command_entry = tk.Entry(root, width=50)
    command_entry.pack(padx=10, pady=5)

    def on_send_command():
        cmd = command_entry.get().strip()
        if cmd:
            command_queue.put(cmd)
            print("Queued command:", cmd)
            command_entry.delete(0, tk.END)

    send_command_button = tk.Button(root, text="Send Command", command=on_send_command)
    send_command_button.pack(padx=10, pady=5)

    video_entry = tk.Entry(root, width=50)
    video_entry.pack(padx=10, pady=5)

    def on_send_video():
        video_cmd = video_entry.get().strip()
        if video_cmd:
            video_queue.put(video_cmd)
            print("Queued video command:", video_cmd)
            video_entry.delete(0, tk.END)

    send_video_button = tk.Button(root, text="Send Video", command=on_send_video)
    send_video_button.pack(padx=10, pady=5)

    root.mainloop()
