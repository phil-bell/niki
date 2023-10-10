import json
import os
import threading
import time
from subprocess import run

import websocket
from qbittorrent import Client

SERVER_URL = os.environ.get("SERVER_URL", "wss://starfish-app-hxdcr.ondigitalocean.app")
SERVER_KEY = os.environ.get("SERVER_KEY", "")
SERVER_SECRET = os.environ.get("SERVER_SECRET", "")
QB_PASSWORD = os.environ.get("QB_PASSWORD", "adminadmin")


def qb_client() -> Client:
    qb = Client("http://0.0.0.0:8080/")
    qb.login("admin", QB_PASSWORD)
    return qb


def torrent_add(content: dict) -> str:
    qb = qb_client()
    message = qb.download_from_link(
        content.get("magnet"),
        savepath=content.get("location"),
    )
    print(f"Torrent added to: {content.get('location')}")
    return message


def router(message: str) -> str | None:
    data = json.loads(message)
    match data.get("type"):
        case "torrent.add":
            return torrent_add(content=data.get("content"))


def on_open(ws) -> None:
    print("Connection open")


def on_message(ws, message: str) -> None:
    threading.Thread(target=router, kwargs={"message": message}).start()


def on_close(ws, close_status_code, close_msg) -> None:
    print("Connection closed")
    if close_status_code or close_msg:
        print(f"{close_status_code}: {close_msg}")


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
