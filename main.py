import pyautogui
from pynput.mouse import Controller
from PIL import ImageGrab
import time
import threading
import tkinter as tk
import configparser

# Create a mouse controller to simulate clicks
mouse_controller = Controller()

# Global variable to track whether the script is running
is_running = False

# Global variable to hold the selected color range
selected_color_range = None

# Define color ranges for Red, Yellow, and Purple
RED_MIN = (150, 0, 0)
RED_MAX = (255, 50, 50)

YELLOW_MIN = (150, 150, 0)
YELLOW_MAX = (255, 255, 100)

PURPLE_MIN = (100, 0, 150)
PURPLE_MAX = (150, 50, 255)

# Load the configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Get the delay time from the config file, default to 0.01 if not set
check_delay = float(config.get('settings', 'check_delay', fallback=0.01))

def is_color_in_range(color, min_range, max_range, tolerance=10):
    """
    Check if the pixel color is within the specified range with a tolerance.
    """
    r, g, b = color
    return (min_range[0] - tolerance <= r <= max_range[0] + tolerance and
            min_range[1] - tolerance <= g <= max_range[1] + tolerance and
            min_range[2] - tolerance <= b <= max_range[2] + tolerance)

def get_color_at_mouse():
    """
    Grab the pixel color at the current mouse position.
    """
    x, y = pyautogui.position()
    
    # Take a screenshot at the mouse position (just a 1x1 region)
    screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    color = screenshot.getpixel((0, 0))  # Get the color of the pixel
    return color

def detect_color_pixels():
    """
    Continuously check the pixel color at the mouse position and click if it matches the selected color.
    This function runs in a separate thread.
    """
    global is_running, selected_color_range
    while is_running:
        color = get_color_at_mouse()
        if selected_color_range and is_color_in_range(color, *selected_color_range):
            print(f"Color detected at {pyautogui.position()}! Left-clicking...")
            pyautogui.click()  # Simulate a left-click at the current mouse position
        time.sleep(check_delay)  # Use the delay from the config file

def start_detection():
    """Start the detection process in a separate thread."""
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=detect_color_pixels, daemon=True).start()
        start_button.config(text="Stop Detection", bg="#e74c3c", fg="white")
        status_label.config(text="Status: Running", fg="green")
    else:
        stop_detection()

def stop_detection():
    """Stop the detection process."""
    global is_running
    is_running = False
    start_button.config(text="Start Detection", bg="#2ecc71", fg="white")
    status_label.config(text="Status: Stopped", fg="red")

def set_red_color_range():
    """Set the color range to detect red."""
    global selected_color_range
    selected_color_range = (RED_MIN, RED_MAX)
    print("Selected color: Red")

def set_yellow_color_range():
    """Set the color range to detect yellow."""
    global selected_color_range
    selected_color_range = (YELLOW_MIN, YELLOW_MAX)
    print("Selected color: Yellow")

def set_purple_color_range():
    """Set the color range to detect purple."""
    global selected_color_range
    selected_color_range = (PURPLE_MIN, PURPLE_MAX)
    print("Selected color: Purple")

# Create the GUI window
root = tk.Tk()
root.title("Python ColorBot")  # Updated window title

# Set the window size and background color to black
root.geometry("700x600")  # Keep the width same but increase the height
root.configure(bg="black")

# Remove the window's title bar and borders
root.overrideredirect(True)

# Add some padding and styling to make it look more refined

# Header Label (Title)
header_label = tk.Label(root, text="Python ColorBot", font=("Helvetica", 24, "bold"), fg="white", bg="black")
header_label.pack(pady=40)

# Create a start/stop button with smaller size
start_button = tk.Button(root, text="Start Detection", command=start_detection, width=15, height=2, font=("Arial", 12), bg="#2ecc71", fg="white", relief="raised")
start_button.pack(pady=10)

# Buttons to choose color ranges
red_button = tk.Button(root, text="Detect Red", command=set_red_color_range, width=15, height=2, font=("Arial", 12), bg="#e74c3c", fg="white", relief="raised")
red_button.pack(pady=5)

yellow_button = tk.Button(root, text="Detect Yellow", command=set_yellow_color_range, width=15, height=2, font=("Arial", 12), bg="#f39c12", fg="white", relief="raised")
yellow_button.pack(pady=5)

purple_button = tk.Button(root, text="Detect Purple", command=set_purple_color_range, width=15, height=2, font=("Arial", 12), bg="#8e44ad", fg="white", relief="raised")
purple_button.pack(pady=5)

# Status label with larger font, change text color to white for contrast against black background
status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 14), fg="red", bg="black")
status_label.pack(pady=20)

# Function to enable dragging of the window
dragging = False
offset_x = 0
offset_y = 0

def start_drag(event):
    """Start dragging: record the position where the mouse is clicked."""
    global dragging, offset_x, offset_y
    dragging = True
    offset_x = event.x
    offset_y = event.y

def stop_drag(event):
    """Stop dragging: reset dragging state."""
    global dragging
    dragging = False

def drag_motion(event):
    """Drag the window: update position based on mouse movement."""
    global offset_x, offset_y
    if dragging:
        x = root.winfo_pointerx() - offset_x
        y = root.winfo_pointery() - offset_y
        root.geometry(f'+{x}+{y}')

# Bind mouse events for dragging
header_label.bind("<Button-1>", start_drag)  # Left-click on header to start dragging
header_label.bind("<ButtonRelease-1>", stop_drag)  # Release the mouse to stop dragging
header_label.bind("<B1-Motion>", drag_motion)  # Move the window when dragging

# Run the Tkinter event loop
root.mainloop()
