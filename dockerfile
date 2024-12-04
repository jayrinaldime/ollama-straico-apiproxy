FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3214

HEALTHCHECK --interval=1m --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3214/docs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3214"]
