FROM python:3.8.3-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD alembic upgrade head && uvicorn ./src/main:application --host 0.0.0.0 --port $PORT --reload
