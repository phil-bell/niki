import json
import logging
import os
import pickle
import shutil
import time
from subprocess import run

import requests
from fastapi import Depends, FastAPI, Request, Response
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey, PublicKey, SealedBox
from qbittorrent import Client

run(["qbittorrent-nox", "-d"])

logger = logging.getLogger("uvicorn.error")
response = requests.get("https://starfish-app-hxdcr.ondigitalocean.app/api/key/")
data = response.json()
NIKI_PUBLIC_KEY = data[0].get("public_key").encode()
QB_PASSWORD = os.environ.get("QB_PASSWORD", "adminadmin")

app = FastAPI()


class MissingPrivateKeyException(Exception):
    def __init__(
        self,
        message="No private key stored locally while loading route that requires it, please restart your server to generate a new private key.",
    ):
        self.message = message
        super().__init__(self.message)


async def decrypt(request: Request) -> dict:
    data: bytes = await request.body()
    with open("PrivateKey", "rb") as private_key_file:
        try:
            key = pickle.load(private_key_file)
        except EOFError:
            raise MissingPrivateKeyException
        box = SealedBox(key)
        decrypted_data = box.decrypt(data)
        return json.loads(decrypted_data.decode())


async def qb_client() -> Client:
    qb = Client("http://0.0.0.0:8080/")
    qb.login("admin", QB_PASSWORD)
    return qb


def encrpyt(data: dict) -> bytes:
    box = SealedBox(PublicKey(NIKI_PUBLIC_KEY, encoder=HexEncoder))
    data_str = json.dumps(data)
    return box.encrypt(data_str.encode())


def box_message(messages: list):
    width, _ = shutil.get_terminal_size()
    line = "".join(["-" for _ in range(width - 10)])
    empty_line = f'|{"".join([" " for _ in range(width - 12)])}|'
    logger.info(line)
    for message in messages[:-1]:
        space = "".join([" " for _ in range((width - len(message) - 12) // 2)])
        logger.info(f"|{space}{message}{space}|")
        logger.info(empty_line)
    space = "".join([" " for _ in range((width - len(messages[-1]) - 12) // 2)])
    logger.info(f"|{space}{messages[-1]}{space}|")
    logger.info(line)


def get_private_key() -> str:
    try:
        logger.info("")
        logger.info("Loading existing public key...")
        file = open("PrivateKey", "rb")
        key = pickle.load(file)
        file.close()
    except (EOFError, FileNotFoundError):
        file = open("PrivateKey", "wb")
        key = PrivateKey.generate()
        pickle.dump(key, file)
        file.close()
        logger.info("Generating new public key...")
    return key.public_key.encode(encoder=HexEncoder).decode()


@app.on_event("startup")
def startup_event():
    key = get_private_key()
    logger.info("")
    box_message(["Public key", key])
    logger.info("")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add/")
async def add(data: dict = Depends(decrypt)):
    qb = await qb_client()
    message = qb.download_from_link(
        data.get("magnet"),
        savepath=data.get("location"),
    )
    encrypted_data = encrpyt({"message": message})
    return Response(content=encrypted_data)


@app.get("/status/")
async def status():
    qb = await qb_client()
    torrents = qb.torrents()
    encrypted_data = encrpyt({"torrents": torrents})
    return Response(content=encrypted_data)
