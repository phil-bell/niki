import os
from subprocess import run

import websocket

import app.handlers as handlers

SERVER_URL = os.environ.get("SERVER_KEY", "wss://octopus-app-74lmf.ondigitalocean.app")
SERVER_KEY = os.environ.get("SERVER_KEY")
SERVER_SECRET = os.environ.get("SERVER_SECRET")


def main():
    websocket.enableTrace(False)
    run(["qbittorrent-nox", "-d"])
    wsapp = websocket.WebSocketApp(
        f"{SERVER_URL}/server/{SERVER_KEY}",
        header={"authentication": SERVER_SECRET},
        on_open=handlers.on_open,
        on_message=handlers.on_message,
        on_close=handlers.on_close,
    )
    wsapp.run_forever()


if __name__ == "__main__":
    main()
