import qbittorrentapi
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
qbittorrent = qbittorrentapi.Client(
    host="localhost",
    port=8080,
    username="admin",
    password="adminadmin",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/download/")
def download(
    magnet: str, name: str, location: str, token: str = Depends(oauth2_scheme)
):
    qbittorrent.torrents_add(
        urls=magnet,
        save_path=f"{location}{name}",
    )
