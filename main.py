import time
import os 
import math 
import json
import sys 
import trio 
from trio_websocket import open_websocket_url, ConnectionClosed, HandshakeError
from contextlib import asynccontextmanager

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

async def servo_worker():
    set_servo_angle(0) 
    print("[servo-worker] starting")
    current_angle = 0
    while True:
        target_angle = count_to_angle(get_shared_count())
        if (current_angle != target_angle): 
            next_angle = step_towards(current_angle, target_angle) 
            set_servo_angle(next_angle)
            current_angle = next_angle
        await trio.sleep(0.01)

# ---- 
# OLED Worker 

async def oled_worker():
    draw_text("...") 
    print("[oled-worker] starting")
    last_count = None
    while True:
        current_count = get_shared_count() 
        if current_count != last_count:
            draw_text(f"{current_count}")
            last_count = current_count 
        await trio.sleep(0.01)

# ------
# Socket Worker 

API_KEY = os.environ.get('INSTOMETER_API_KEY') 

async def ws_open_handler(ws): 
    print("[ws] connection opened")
    init_message = json.dumps({
        "type": "init", 
        "token": API_KEY
    })
    await ws.send_message(init_message)

async def ws_message_handler(ws):
    while True:
        message = await ws.get_message()
        print("[ws] message", message)
        m = json.loads(message)
        count = m['count']
        set_shared_count(count) 

async def websocket_worker(): 
    sleep_secs = 5
    max_reconnects = 12
    num_reconnects = 0
    ws_uri = 'wss://api.instantdb.com/dash/session_counts' 
    while True: 
        try:
            async with open_websocket_url(ws_uri) as ws:
                await ws_open_handler(ws)
                await ws_message_handler(ws)
        except (ConnectionClosed, HandshakeError) as e:
            num_reconnects += 1
            if num_reconnects > max_reconnects:
                raise e
            print(f"[ws] reconnecting in {sleep_secs} seconds")
            await trio.sleep(sleep_secs)

# ----
# Main 

async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(servo_worker)
        nursery.start_soon(oled_worker)
        nursery.start_soon(websocket_worker) 
   
if __name__ == "__main__":
    def shutdown_hardware():
        set_servo_angle(0)
        draw_text("...")
    try: 
        trio.run(main) 
    except KeyboardInterrupt:
        shutdown_hardware()
        print("goodbye :)")
        sys.exit(0)
    except Exception as e:
        shutdown_hardware()
        draw_text("err :<")
        raise e
