import functools
import json
import logging
import os

import requests
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from jprq import __version__
from jprq.tunnel_http import open_http_tunnel

logger = logging.getLogger("uvicorn.error")
app = FastAPI()


def credentials(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with open("creds.json", "r", encoding="utf-8") as json_file:
            try:
                creds = json.load(json_file)
            except json.decoder.JSONDecodeError:
                creds = {}
        func(creds, *args, **kwargs)

    return wrapper


@app.on_event("startup")
@credentials
def startup_event(creds):
    if "key" not in creds.keys():
        key = input("Please enter your server key: ")
        creds["key"] = key
    if "secret" not in creds.keys():
        secret = input("Please enter your secret: ")
        creds["secret"] = secret

    with open("creds.json", "w", encoding="utf-8") as json_file:
        json.dump(creds, json_file, ensure_ascii=False, indent=4)


@app.get("/")
def read_root():
    return {"Hello": "World"}
