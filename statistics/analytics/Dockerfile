# chatbot_api/Dockerfile

FROM python:3.9.13-slim

WORKDIR /app
COPY ./src/ /app

COPY ./pyproject.toml /app/pyproject.toml
COPY ./.env /app/.env
RUN pip install /app/.

EXPOSE 8032
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8032"]