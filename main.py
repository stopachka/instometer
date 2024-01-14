from time import sleep
import threading
import os 
import math 

USE_REAL_HARDWARE = not os.environ.get('INSTOMETER_VIRTUAL_HARDWARE')

# -----
# Servo 

if USE_REAL_HARDWARE: 
    from servo import set_servo_angle 
else: 
    def set_servo_angle(angle): 
        print(f"[virtual-servo] set angle = {angle}") 

# ----- 
# OLED 

if USE_REAL_HARDWARE: 
    from oled import draw_text 
else: 
    def draw_text(text): 
        print(f"[virtual-oled] draw text = {text}") 

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
    return 10 ** math.ceil(
        math.log10(
            max(2, count)
        )
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

API_KEY = os.environ.get('INSTOMETER_API_KEY') 

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

