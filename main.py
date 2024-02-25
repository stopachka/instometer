import time
import os 
import math 
import json
import sys 
import trio 
from trio_websocket import open_websocket_url, ConnectionClosed, HandshakeError
from screen import draw_screen 
from log import log

USE_REAL_HARDWARE = not os.environ.get('INSTOMETER_VIRTUAL_HARDWARE')

# -----
# Servo 

if USE_REAL_HARDWARE: 
    from servo import set_servo_angle 
else: 
    def set_servo_angle(angle): 
        log.info("[virtual-servo] set angle = %s", angle) 

# ------
# Shared Data 

shared_status = 'initializaing'

shared_report = {} 

def set_shared_report(new_report):
    global shared_report
    shared_report = new_report 

def get_shared_report():
    return shared_report 

def total_count(report):
    return sum([r['count'] for r in report.values()]) 

def get_shared_status(): 
    return shared_status 

def set_shared_status(status):
    global shared_status 
    shared_status = status

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
    log.info("[servo-worker] starting")
    current_angle = 0
    while True:
        target_angle = count_to_angle(total_count(get_shared_report()))
        if (current_angle != target_angle): 
            next_angle = step_towards(current_angle, target_angle) 
            set_servo_angle(next_angle)
            current_angle = next_angle
        await trio.sleep(0.01)

# ---- 
# Screen Worker 

async def screen_worker():
    log.info("[screen-worker] starting")
    last_report = None
    last_status = None 
    while True:
        current_report = get_shared_report()
        current_status = get_shared_status()
        if current_report != last_report or last_status != current_status:
            draw_screen(
                current_status,
                current_report, 
                total_count(current_report)
            )
            last_report = current_report
            last_status = current_status
        await trio.sleep(0.01)

# ------
# Socket Worker 

API_KEY = os.environ.get('INSTOMETER_API_KEY') 

async def ws_handle_open(ws): 
    log.info("[ws] init")
    init_message = json.dumps({
        "type": "init", 
        "token": API_KEY
    })
    await ws.send_message(init_message)

async def ws_message_worker(ws):
    while True:
        message = await ws.get_message()
        log.info("[ws] message = %s", message)
        m = json.loads(message)
        # (XXX) 
        # We currently get some empty sessions. 
        # We should clean these up at the source, but 
        # for now we'll just ignore them here.
        report = m['report']
        report.pop("", None) 
        set_shared_report(report) 

async def ws_heartbeat_worker(ws, timeout_secs=10, interval_secs=5):
    while True: 
        with trio.fail_after(timeout_secs):
            await ws.ping()
        await trio.sleep(interval_secs) 

async def websocket_worker(): 
    sleep_secs = 5
    ws_uri = 'wss://api.instantdb.com/dash/session_counts' 
    while True: 
        try:
            async with open_websocket_url(ws_uri) as ws:
                set_shared_status("connected")
                await ws_handle_open(ws)
                async with trio.open_nursery() as nursery:
                    nursery.start_soon(ws_heartbeat_worker, ws)
                    nursery.start_soon(ws_message_worker, ws) 
        except (ConnectionClosed, HandshakeError) as e:
            set_shared_status("disconnected")
            log.info(
                "[ws] reconnecting in %s seconds", 
                sleep_secs, 
                exc_info=True
            )
            await trio.sleep(sleep_secs)

# ----
# Main 

async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(servo_worker)
        nursery.start_soon(screen_worker)
        nursery.start_soon(websocket_worker) 
   
if __name__ == "__main__":
    def shutdown_hardware():
        set_servo_angle(0)
    try: 
        trio.run(main) 
    except KeyboardInterrupt:
        shutdown_hardware()
        log.info("goodbye :)")
        sys.exit(0)
    except Exception as e:
        shutdown_hardware()
        log.error("Uncaught error", exc_info=True)
        raise e
