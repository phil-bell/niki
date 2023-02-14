FROM python:3.11-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev && \
    apk add --no-cache qbittorrent-nox && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del .pynacl_deps

COPY . /code/

# ENTRYPOINT ["/code/docker-entrypoint.sh"]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
CMD ["/bin/bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload & qbittorrent-nox -d"]

# Build:
# docker build -t niki-server .

# Start:
# docker create -v $(pwd):/code -p 8004:8004 --name niki-server niki-server
# docker start -ia niki-server
# docker run --tty -v $(pwd):/code -p 8004:8004 --name niki-server niki-server
# docker run --name tunnel-proxy --env PORTS="8004:3004" -itd --net=host vitobotta/docker-tunnel:0.31.0 proxy
# uvicorn app.main:app --host 0.0.0.0 --port 8002