import websocket
import _thread
import time
import rel
import json
from gpiozero import Servo
from time import sleep
import os 

# Config 

API_KEY = os.environ.get('SESSION_COUNTER_API_KEY') 

# Servo 

servo = Servo(17)

# Sockets

def get_value(n): 
    dec = min(n / 5, 1) 
    scaled = 2 * dec - 1 
    return scaled

def on_message(ws, message):
    m = json.loads(message)
    count = m['count'] 
    servo.value = get_value(count) 

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    init_message = json.dumps({"type": "init", "token": API_KEY})
    ws.send(init_message)

if __name__ == "__main__":
    servo.value = -1 
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api.instantdb.com/dash/session_counts",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch() 

