from app.bittorrent import qb_client


def torrent_add(content: dict) -> str:
    qb = qb_client()
    message = qb.download_from_link(
        content.get("magnet"),
        savepath=content.get("location"),
    )
    print(f"Torrent added to: {content.get('location')}")
    return message
