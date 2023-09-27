import threading

from app.urls import router


def on_open(ws) -> None:
    print("Connection open")


def on_message(ws, message: str) -> None:
    threading.Thread(target=router, kwargs={"message": message}).start()


def on_close(ws, close_status_code, close_msg) -> None:
    print("Connection closed")
    if close_status_code or close_msg:
        print(f"{close_status_code}: {close_msg}")
