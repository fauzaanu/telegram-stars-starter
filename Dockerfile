FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
RUN pip install poetry && poetry config virtualenvs.create false
COPY . /app/
RUN ls /app/
RUN poetry install --no-interaction --no-root
CMD ["poetry", "run", "python", "bot.py"]
