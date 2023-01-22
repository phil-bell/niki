import functools
import json
import logging
import pickle

import requests
from fastapi import FastAPI
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey, SealedBox
from pydantic import BaseModel
from qbittorrent import Client

NIKI_PUBLIC_KEY = ""

logger = logging.getLogger("uvicorn.error")
app = FastAPI()
qb = Client("http://0.0.0.0:8080/")
qb.login("admin", "adminadmin")


class MissingPrivateKeyException(Exception):
    def __init__(
        self,
        message="No private key stored locally while loading route that requires it, please restart your server to generate a new private key.",
    ):
        self.message = message
        super().__init__(self.message)


def decrypt(data: str):
    with open("PrivateKey", "rb") as private_key_file:
        try:
            key = pickle.load(private_key_file)
        except EOFError:
            raise MissingPrivateKeyException
        box = SealedBox(key)
        box.decrypt(data)
        return json.loads(data.dencode("utf-8"))


def encrpyt(data: dict):
    box = SealedBox(NIKI_PUBLIC_KEY)
    return box.encrpyt(json.dumps(data).encode("utf-8"))


@app.on_event("startup")
def startup_event():
    try:
        file = open("PrivateKey", "rb")
        key = pickle.load(file)
        file.close()
        logger.info("Loading existing public key: ")
    except EOFError:
        file = open("PrivateKey", "wb")
        key = PrivateKey.generate()
        pickle.dump(key, file)
        file.close()
        logger.info("Generating new public key:")
    logger.info(key.public_key.encode(encoder=HexEncoder).decode("utf-8"))


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("add/")
async def add(data: str):
    torrent = decrypt(data)
    return {"torrents": torrents}


@app.get("status/")
async def status():
    torrents = qb.torrents()
    return encrpyt(torrents)
