import tkinter as tk
from earth_base.config import *


def start_gui(command_queue_1, command_queue_2, video_queue):
    root = tk.Tk()
    root.title("Earth Base - Command Input")

    def on_send_command():
        cmd = command_entry_1.get().strip()
        if cmd:
            command_queue_1.put(cmd)
            print("Queued command 1:", cmd)
            command_entry_1.delete(0, tk.END)

        cmd = command_entry_2.get().strip()
        if cmd:
            command_queue_2.put(cmd)
            print("Queued command 2:", cmd)
            command_entry_2.delete(0, tk.END)

        video_cmd = video_entry.get().strip()
        if video_cmd:
            video_queue.put(video_cmd)
            print("Queued video command:", video_cmd)
            video_entry.delete(0, tk.END)

    command_entry_1 = tk.Entry(root, width=50)
    command_entry_1.pack(padx=10, pady=5)

    command_entry_2 = tk.Entry(root, width=50)
    command_entry_2.pack(padx=10, pady=5)

    video_entry = tk.Entry(root, width=50)
    video_entry.pack(padx=10, pady=5)

    send_button = tk.Button(root, text="Send Commands", command=on_send_command)
    send_button.pack(padx=10, pady=5)

    root.mainloop()
