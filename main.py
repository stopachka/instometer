from time import sleep
import threading

# -----
# Servo 

from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

min_pulse_width = 0.0005  #  0.5ms
max_pulse_width = 0.0025  #  2.5ms
factory = PiGPIOFactory() #  reduces jitter

servo = AngularServo(
    17, 
    min_pulse_width=min_pulse_width, 
    max_pulse_width=max_pulse_width, 
    min_angle=0, 
    max_angle=180,
    pin_factory=factory
)

def set_servo_angle(angle): 
    print(f"[servo] set angle {angle}")
    # the servo is physically positioned 
    # in such a way, that the angle 0 looks 
    # like the angle 180.
    servo.angle = 180 - angle 

# ----- 
# OLED 

import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
font = ImageFont.truetype("arialbd.ttf", size=22)

def text_to_image(text):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    # set text
    (font_width, font_height) = font.getsize(text)
    text_pos_x = oled.width // 2 - font_width // 2 
    text_pos_y = oled.height // 2 - font_height // 2  
    draw.text(
        (text_pos_x, text_pos_y),
        text,
        font=font,
        fill=255,
    )
    return image 

def draw_image(image): 
    oled.image(image) 
    oled.show() 

def draw_text(text): 
    print(f"[oled] draw text = {text}")
    draw_image(text_to_image(text))

# ------
# Counter 

shared_count = 0 

def set_shared_count(new_count):
    global shared_count
    shared_count = new_count 

def get_shared_count():
    return shared_count 


# -------------
# Servo Worker 

def choose_denominator(count): 
    if (count < 50):
        return 50 

    return 10 ** math.ceil(
        math.log10(count)
    )

def frac_to_angle(count, denominator): 
    dec = min(count / denominator, 1) 
    scaled = 180 * dec 
    return scaled

def count_to_angle(count): 
    denom = choose_denominator(count)
    return frac_to_angle(count, denom) 

def step_towards(start_angle, end_angle): 
    num_left = end_angle - start_angle 
    step = math.copysign(1, num_left)
    
    new_angle = start_angle + step 
    
    if math.isclose(new_angle, end_angle, abs_tol=1):
        new_angle = end_angle
    
    return new_angle 

def servo_worker():
    set_servo_angle(0) 
    print("[servo-worker] starting")
    current_angle = 0
    while True:
        target_angle = count_to_angle(get_shared_count())
        if (current_angle != target_angle): 
            next_angle = step_towards(current_angle, target_angle) 
            set_servo_angle(next_angle)
            current_angle = next_angle
        
        time.sleep(0.01)

def oled_worker():
    draw_text("...") 
    print("[oled-worker] starting")
    last_count = None
    while True:
        current_count = get_shared_count() 
        if current_count != last_count:
            draw_text(f"{current_count}")
            last_count = current_count 
        time.sleep(0.01)

# ------
# Sockets 

import websocket
import _thread
import time
import rel
import json
import os 
import math 

API_KEY = os.environ.get('SESSION_COUNTER_API_KEY') 

def on_message(ws, message):
    print("[ws] message", message) 
    m = json.loads(message)
    count = m['count'] 
    set_shared_count(count) 

def on_error(ws, error):
    print("[ws] error", error)

def on_close(ws, close_status_code, close_msg):
    print("[ws] conn closed")

def on_open(ws):
    print("[ws] init")
    init_message = json.dumps({
        "type": "init", 
        "token": API_KEY
    })
    ws.send(init_message)

if __name__ == "__main__":
    servo_thread = threading.Thread(target=servo_worker, daemon=True)
    servo_thread.start()

    oled_thread = threading.Thread(target=oled_worker, daemon=True)
    oled_thread.start()
 
    ws = websocket.WebSocketApp(
        "wss://api.instantdb.com/dash/session_counts", 
        on_open=on_open, 
        on_message=on_message, 
        on_error=on_error, 
        on_close=on_close
    )
    ws.run_forever(
        dispatcher=rel, 
        reconnect=5, 
        ping_interval=10,
    )  
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch() 

