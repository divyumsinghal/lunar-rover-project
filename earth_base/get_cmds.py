import tkinter as tk
import queue
from earth_base.config import *


def start_gui(
    command_queue_1,
    command_queue_2,
    command_queue_3,
    command_queue_4,
    video_queue,
):
    root = tk.Tk()
    root.title("Earth Base - Command Input")

    def on_send_command():
        command_entries = [
            (command_entry_1, command_queue_1, "Command Entry 1"),
            (command_entry_2, command_queue_2, "Command Entry 2"),
            (command_entry_3, command_queue_3, "Command Entry 3"),
            (command_entry_4, command_queue_4, "Command Entry 4"),
            (video_entry, video_queue, "Video Entry"),
        ]

        for entry, queue, placeholder in command_entries:
            cmd = entry.get().strip()
            if cmd and cmd != placeholder:
                queue.put(cmd)
                print(f"Queued: {cmd}")
                entry.delete(0, tk.END)

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

    # Creating and adding placeholders for entries
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

    listbox = tk.Listbox(root, width=40, height=80)
    listbox.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)

    def update_queue_display():
        try:
            while not sensor_data_recv_queue.empty():
                item = sensor_data_recv_queue.get_nowait()
                listbox.insert(tk.END, item)
        except queue.Empty:
            pass
        root.after(100, update_queue_display)

    update_queue_display()
    root.mainloop()
