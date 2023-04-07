import json
import logging
import pickle
import shutil
import time

import requests
from fastapi import Depends, FastAPI, Request, Response

# from cryptography.fernet import Fernet
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey, PublicKey, SealedBox
from qbittorrent import Client

logger = logging.getLogger("uvicorn.error")
app = FastAPI()
qb = Client("http://0.0.0.0:8080/")
qb.login("admin", "adminadmin")

response = requests.get("http://host.docker.internal:8000/api/key/")
data = response.json()
NIKI_PUBLIC_KEY = data[0].get("public_key").encode()


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


@app.on_event("startup")
def startup_event():
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
    logger.info("")
    box_message(
        [
            "Public key",
            key.public_key.encode(encoder=HexEncoder).decode(),
        ]
    )
    logger.info("")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add/")
async def add(data: dict = Depends(decrypt)):
    message = qb.download_from_link(
        data.get("magnet"),
        savepath=data.get("location"),
    )
    encrypted_data = encrpyt({"message": message})
    return Response(content=encrypted_data)


@app.get("/status/")
async def status():
    torrents = qb.torrents()
    encrypted_data = encrpyt({"torrents": torrents})
    return Response(content=encrypted_data)
