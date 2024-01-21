FROM python:3.11-alpine

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt /app

RUN python -m pip install -r requirements.txt

COPY reddit_api/ /app/reddit_api

CMD ["python", "-m", "reddit_api"]
