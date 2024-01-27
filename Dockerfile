FROM python:3.11-slim

WORKDIR /app

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /app/

RUN pdm export --prod --without-hashes -f requirements -o requirements.txt; \
    pip install -U -r requirements.txt

COPY reddit_api/ /app/reddit_api

CMD ["python", "-m", "reddit_api"]

