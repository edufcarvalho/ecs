FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apk add gcc musl-dev libpq-dev git
RUN pip install -r requirements.txt
RUN python -m pip install --break-system-packages git+https://github.com/dpkp/kafka-python.git

CMD ["fastapi", "dev", "/app/ecs/main.py"]
