import json

from app.views import torrent_add


def router(message: str) -> str | None:
    data = json.loads(message)
    match data.get("type"):
        case "torrent.add":
            return torrent_add(content=data.get("content"))
