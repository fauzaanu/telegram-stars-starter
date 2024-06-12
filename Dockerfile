FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
RUN pip install poetry && poetry config virtualenvs.create false
COPY . /app/
RUN ls /app/
RUN poetry install --no-interaction --no-root
ENV TELEGRAM_BOT_TOKEN ${TELEGRAM_BOT_TOKEN}
RUN poetry run python bot.py
