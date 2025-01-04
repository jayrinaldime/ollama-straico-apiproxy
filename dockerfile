FROM python:3.12

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && apt-get install -y docker.io \
    && rm -rf /var/lib/apt/lists/*

# Mount Docker socket
VOLUME /var/run/docker.sock

COPY . /app

EXPOSE 3214

HEALTHCHECK --interval=1m --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3214/docs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3214"]
