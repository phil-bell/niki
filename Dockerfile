FROM python:3.11-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . /code/

ENV BACKEND_URL=http://127.0.0.1:8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]

# Build:
# docker build -t niki-server .

# Start:
# docker run -it --network host -p 8003:8003 -p 8002:8002 -v $(pwd):/code niki-server

# uvicorn app.main:app --host 0.0.0.0 --port 8002