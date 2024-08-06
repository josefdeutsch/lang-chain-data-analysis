# Use Python 3.9 slim as the base image
FROM python:3.9.13-slim

WORKDIR /app

COPY ./src/ /app

COPY ./pyproject.toml /code/pyproject.toml
COPY ./.env /app/.env
RUN pip install /code/.

CMD ["sh", "entrypoint.sh"]