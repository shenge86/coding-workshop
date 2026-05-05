FROM python:3.12-slim

WORKDIR /app

ENV HF_HOME=/root/.cache/huggingface \
    PIP_DEFAULT_TIMEOUT=180

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/images /app/chroma_data

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
