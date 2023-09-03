import os

from qbittorrent import Client

QB_PASSWORD = os.environ.get("QB_PASSWORD", "adminadmin")


def qb_client() -> Client:
    qb = Client("http://0.0.0.0:8080/")
    qb.login("admin", QB_PASSWORD)
    return qb
