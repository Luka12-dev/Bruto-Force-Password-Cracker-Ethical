import tkinter as tk
from tkinter import ttk
import itertools
import string
import threading
import time

update_interval = 1110455555555
characters = string.ascii_lowercase + string.digits
max_length = 7

def start_brutoforce(event=None):
    password = password_entry.get()
    if not password:
        status_var.set("⚠️ Please enter a password")
        return

    if len(password) > max_length:
        status_var.set(f"⚠️ Password too long for brute-force (max {max_length} characters).")
        return

    start_button.config(state=tk.DISABLED)
    status_var.set("⏳ Starting brute-force...")

    def run():
        bruteforce(password, lambda msg: status_var.set(msg))
        start_button.config(state=tk.NORMAL)

    threading.Thread(target=run, daemon=True).start()


def bruteforce(password, update_status):
    global update_interval
    attempts = 0
    start_time = time.time()

    for length in range(1, max_length + 1):
        for combination in itertools.product(characters, repeat=length):
            guess = ''.join(combination)
            attempts += 1

            if attempts % update_interval == 0:
                update_status(f"Attempt #{attempts}: {guess}")

            if guess == password:
                duration = round(time.time() - start_time, 2)
                update_status(f"✅ Password found: '{guess}' in {duration} seconds ({attempts} attempts)")
                return

    update_status("❌ Password not found.")


# --- GUI Setup ---
window = tk.Tk()
window.title("Brute-Force Password Cracker")
window.geometry("500x305")
window.configure(bg="black")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="white", foreground="black",
                font=("Segoe UI", 11), padding=6, borderwidth=0)
style.map("TButton", background=[("active", "#e0e0e0")])

# Title label
title_label = tk.Label(window, font=("Segoe UI", 12), width=30,
                       bg="white", fg="black", text="Enter password (for test):")
title_label.pack(pady=10)

# Password entry
password_entry = tk.Entry(window, font=("Segoe UI", 12), width=30,
                          show="*", bg="black", fg="white", insertbackground="white",
                          highlightthickness=1, highlightbackground="white")
password_entry.pack(pady=10)

# Start button
start_button = ttk.Button(window, text="Start BruteForce", command=start_brutoforce)
start_button.pack(pady=10)

# Bind Enter to start start_bruto-force function
window.bind('<Return>', start_brutoforce)

# Status label
status_var = tk.StringVar()
status_label = tk.Label(window, textvariable=status_var, wraplength=480,
                        bg="black", fg="white", font=("Segoe UI", 10))
status_label.pack(pady=10)

# Start GUI loop
window.mainloop()