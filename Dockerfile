FROM python:3.11-alpine

WORKDIR /code

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /code/requirements.txt

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev && \
    apk add --no-cache qbittorrent-nox && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del .pynacl_deps && \
    rm /code/requirements.txt

COPY main.py /code/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

# docker run -d -v /mnt/a/movie/:/mnt/a/movie/ -v /mnt/c/tv/:/mnt/c/tv/ --network host philbell/niki-server:latest