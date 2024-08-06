FROM python:3.11-slim

WORKDIR /app

COPY ./src/ /app

COPY ./pyproject.toml /code/pyproject.toml
COPY ./.env /app/.env
RUN pip install /code/.

CMD ["sh", "entrypoint.sh"]