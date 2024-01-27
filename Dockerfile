FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y cron

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /app/

RUN pdm export --prod --without-hashes -f requirements -o requirements.txt; \
    pip install -U -r requirements.txt

COPY reddit_api/ /app/reddit_api

#CMD ["sh", "-c", "echo '*/5 * * * * cd /app && python -m reddit_api >> /var/log/reddit_api.log 2>&1' | crontab - && cron -f"]
CMD ["python", "-m", "reddit_api"]

