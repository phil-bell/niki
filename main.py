import json
import logging
import pickle
import shutil

from fastapi import Depends, FastAPI, Request

# from cryptography.fernet import Fernet
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey, PublicKey, SealedBox
from qbittorrent import Client

NIKI_PUBLIC_KEY = b""

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


async def decrypt(request: Request):
    data: bytes = await request.body()
    with open("PrivateKey", "rb") as private_key_file:
        try:
            key = pickle.load(private_key_file)
        except EOFError:
            raise MissingPrivateKeyException
        box = SealedBox(key)
        decrypted_data = box.decrypt(data)
        return json.loads(decrypted_data.decode())


def encrpyt(data: str):
    box = SealedBox(PublicKey(NIKI_PUBLIC_KEY))
    return box.encrypt(json.dumps(data).encode())


def box_message(messages):
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
        logger.info("Loading existing public key:")
        file = open("PrivateKey", "rb")
        key = pickle.load(file)
        file.close()
    except (EOFError, FileNotFoundError):
        file = open("PrivateKey", "wb")
        key = PrivateKey.generate()
        pickle.dump(key, file)
        file.close()
        logger.info("Generating new public key:")
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
async def add(data: bytes = Depends(decrypt)):
    return {"torrents": data}


@app.get("/status/")
async def status():
    torrents = qb.torrents()
    return encrpyt(torrents)


# def new_decrypt(data: str):
#     with open("PrivateKey", "rb") as private_key_file:
#         try:
#             key = pickle.load(private_key_file)
#         except EOFError:
#             raise MissingPrivateKeyException
#         box = SealedBox(key)
#         decrypted_data = box.decrypt(data)
#         return json.loads(decrypted_data.decode())

# def new_encrypt(data:dict):
#     f = Fernet(NIKI_PUBLIC_KEY.encode())
#     return f.encrypt(json.dumps(data).encode())
