FROM python:3.11-alpine

WORKDIR /code

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /code/requirements.txt

RUN apk add --no-cache qbittorrent-nox && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm /code/requirements.txt

COPY main.py /code/main.py

CMD ["python", "main.py"]

# docker build -t

# docker run \
# -d \
# -v /mnt/a/movie/:/mnt/a/movie/ \
# -v /mnt/c/tv/:/mnt/c/tv/ \
# -e SERVER_KEY=abc
# -e SERVER_SECRET=xyz
# --network host \
# philbell/niki-server:latest