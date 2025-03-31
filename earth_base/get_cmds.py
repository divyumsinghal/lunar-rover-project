import tkinter as tk
from earth_base.config import *


def start_gui(
    command_queue_1, command_queue_2, command_queue_3, command_queue_4, video_queue
):
    root = tk.Tk()
    root.title("Earth Base - Command Input")

    def on_send_command():
        cmd = command_entry_1.get().strip()
        if cmd and cmd != "Command Entry 1":
            command_queue_1.put(cmd)
            print("Queued command 1:", cmd)
            command_entry_1.delete(0, tk.END)

        cmd = command_entry_2.get().strip()
        if cmd and cmd != "Command Entry 2":
            command_queue_2.put(cmd)
            print("Queued command 2:", cmd)
            command_entry_2.delete(0, tk.END)

        cmd = command_entry_3.get().strip()
        if cmd and cmd != "Command Entry 3":
            command_queue_3.put(cmd)
            print("Queued command 3:", cmd)
            command_entry_3.delete(0, tk.END)

        cmd = command_entry_4.get().strip()
        if cmd and cmd != "Command Entry 4":
            command_queue_4.put(cmd)
            print("Queued command 4:", cmd)
            command_entry_4.delete(0, tk.END)

        video_cmd = video_entry.get().strip()
        if video_cmd and video_cmd != "Video Entry":
            video_queue.put(video_cmd)
            print("Queued video command:", video_cmd)
            video_entry.delete(0, tk.END)

    def add_placeholder(entry, placeholder):
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda event: restore_placeholder(entry, placeholder))

    def clear_placeholder(entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def restore_placeholder(entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)

    command_entry_1 = tk.Entry(root, width=50)
    command_entry_1.pack(padx=10, pady=5)
    add_placeholder(command_entry_1, "Command Entry 1")

    command_entry_2 = tk.Entry(root, width=50)
    command_entry_2.pack(padx=10, pady=5)
    add_placeholder(command_entry_2, "Command Entry 2")

    command_entry_3 = tk.Entry(root, width=50)
    command_entry_3.pack(padx=10, pady=5)
    add_placeholder(command_entry_3, "Command Entry 3")

    command_entry_4 = tk.Entry(root, width=50)
    command_entry_4.pack(padx=10, pady=5)
    add_placeholder(command_entry_4, "Command Entry 4")

    video_entry = tk.Entry(root, width=50)
    video_entry.pack(padx=10, pady=5)
    add_placeholder(video_entry, "Video Entry")

    send_button = tk.Button(root, text="Send Commands", command=on_send_command)
    send_button.pack(padx=10, pady=5)

    root.mainloop()
