from os import fsdecode, fsync
import websocket
import _thread
import time
import rel

import json

global symbolByChanID
global currency
global chanId
global symbol

symbolByChanID = None
currency = None
chanId = None
symbol = None

def on_message(ws, message):
    
    jsonmsg = json.loads(message)

    currency = jsonmsg['currency']
    symbol = jsonmsg['symbol']
    chanId = jsonmsg['chanId']

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print(symbolByChanID, currency , chanId, symbol)

def on_open(ws):
    print("Opened connection")
    send_json = {"event": "subscribe",
                "channel": "trades",
                "symbol": "fUSD"}
    ws.send(json.dumps(send_json))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api-pub.bitfinex.com/ws/2",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    
    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()