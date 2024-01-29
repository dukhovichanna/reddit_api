FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y cron

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /app/

RUN pdm export --prod --without-hashes -f requirements -o requirements.txt; \
    pip install -U -r requirements.txt

COPY reddit_api/ /app/reddit_api

COPY crontab /etc/cron.d/crontab

COPY run.sh  /app/

RUN chmod 0644 /etc/cron.d/crontab

RUN crontab /etc/cron.d/crontab


ENTRYPOINT [ "/app/run.sh" ]
CMD ["cron","-f", "-l", "2"]

