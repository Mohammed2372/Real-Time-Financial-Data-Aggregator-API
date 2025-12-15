import websocket
import json


# define websocket url
WS_URL = "ws://127.0.0.1:8000/ws/prices/"


def on_message(ws, message):
    data = json.loads(message)
    print(f"🔴 LIVE UPDATE: {data['symbol']} is ${data['price']}")


def on_error(ws, error):
    print(f"🔴 ERROR: {error}")


def on_close(ws, close_status_code, close_msg):
    print("### Connection Closed ###")


def on_open(ws):
    print("✅ Connected to Django Server! Waiting for prices...")


if __name__ == "__main__":
    # connect to server and keep listening forever
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()
