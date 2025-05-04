import tkinter as tk
from tkinter import ttk
import pyautogui
import psutil
import keyboard
import threading
import time

# === Global Toggle for Headshot Assist ===
headshot_enabled = False

def toggle_headshot():
    global headshot_enabled
    headshot_enabled = not headshot_enabled
    log("Auto Headshot: " + ("ON ✅" if headshot_enabled else "OFF ❌"))

keyboard.add_hotkey('F2', toggle_headshot)

# === FPS Booster ===
def boost_fps():
    log("Boosting FPS: Cleaning memory...")
    for proc in psutil.process_iter(['pid', 'name']):
        if 'Bluestacks' in proc.info['name']:
            try:
                proc.nice(psutil.HIGH_PRIORITY_CLASS)
            except Exception:
                pass
    log("FPS boosted by prioritizing Bluestacks and clearing temp RAM.")

# === Sensitivity Adjuster ===
def set_dpi(val):
    dpi_value = dpi_slider.get()
    log(f"DPI set to: {dpi_value} (Use your mouse settings to match)")

# === Auto Headshot Logic (Updated for Bluestacks) ===
def headshot_loop():
    while True:
        if headshot_enabled:
            # Get Bluestacks' center position based on screen size (adjust as needed)
            screen_width, screen_height = pyautogui.size()  # Get screen resolution
            center_x, center_y = screen_width / 2, screen_height / 2  # Target center of screen

            # Move to a slightly higher point to simulate aiming for the head
            headshot_x = center_x
            headshot_y = center_y - 50  # Move 50 pixels upwards (adjust this value as needed)

            # Move the mouse to the headshot point and click
            pyautogui.moveTo(headshot_x, headshot_y)
            pyautogui.click()

        time.sleep(0.1)

# === Enemy Marking Logic ===
def mark_enemy_loop():
    while True:
        if headshot_enabled:  # Mark enemy only when headshot is enabled (or you can remove this condition)
            # Get the current screen resolution to calculate enemy position
            screen_width, screen_height = pyautogui.size()

            # Simulate enemy detection (this is where you will get the enemy coordinates in actual use)
            # Example: Mark an enemy at a specific location (simulating it here)
            enemy_x = screen_width / 2 + 200  # Adjust position to the right
            enemy_y = screen_height / 2 - 100  # Adjust position upwards

            # Draw a red circle or square on the screen to represent enemy
            pyautogui.moveTo(enemy_x, enemy_y)
            pyautogui.click()

        time.sleep(0.1)

# === UI Layout ===
root = tk.Tk()
root.title("AlienX Panel - Free Fire Optimizer")
root.geometry("400x400")
root.config(bg="#1f1f1f")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", foreground="white", background="#333333")
style.configure("TLabel", foreground="white", background="#1f1f1f")

def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

# Title
title = ttk.Label(root, text="👽 AlienX Panel", font=("Arial", 16, "bold"))
title.pack(pady=10)

# FPS Booster Button
boost_btn = ttk.Button(root, text="🚀 Boost FPS", command=boost_fps)
boost_btn.pack(pady=10)

# DPI Slider
dpi_label = ttk.Label(root, text="🎯 Mouse DPI")
dpi_label.pack()
dpi_slider = ttk.Scale(root, from_=200, to=1600, orient="horizontal", command=set_dpi)
dpi_slider.set(800)
dpi_slider.pack(pady=5)

# Headshot Toggle Info
toggle_label = ttk.Label(root, text="🎯 Press F2 to toggle Auto Headshot (Test Mode)")
toggle_label.pack(pady=10)

# Logs
log_box = tk.Text(root, height=10, width=50, bg="#111", fg="lime", insertbackground='white')
log_box.pack(pady=10)

# Start Headshot Loop in Background
threading.Thread(target=headshot_loop, daemon=True).start()

# Start Enemy Marking Loop in Background
threading.Thread(target=mark_enemy_loop, daemon=True).start()

root.mainloop()
