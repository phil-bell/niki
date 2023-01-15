FROM python:3.11-alpine

WORKDIR /code

RUN apk add -U wireguard-tools curl

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . /code/

ENTRYPOINT ["/code/docker-entrypoint.sh"]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]

# Build:
# docker build -t niki-server .

# Start:
# docker create -v $(pwd):/code -p 8004:8004 --name niki-server niki-server
# docker start -ia niki-server
# docker run --name tunnel-proxy --env PORTS="8004:3004" -itd --net=host vitobotta/docker-tunnel:0.31.0 proxy
# uvicorn app.main:app --host 0.0.0.0 --port 8002