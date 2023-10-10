import os
from subprocess import run
import time

import websocket

from app.handlers import on_close, on_message, on_open

SERVER_URL = os.environ.get("SERVER_URL", "wss://starfish-app-hxdcr.ondigitalocean.app")
SERVER_KEY = os.environ.get("SERVER_KEY", "")
SERVER_SECRET = os.environ.get("SERVER_SECRET", "")


def main():
    websocket.enableTrace(True)
    run(["qbittorrent-nox", "-d"])
    while True:
        ws = websocket.WebSocketApp(
            f"{SERVER_URL}/server/{SERVER_KEY}",
            header={"authentication": SERVER_SECRET},
            on_open=on_open,
            on_message=on_message,
            on_close=on_close,
        )
        ws.run_forever(reconnect=1)
        print("Sleeping...")
        time.sleep(5)
        print("Restarting")

if __name__ == "__main__":
    main()
