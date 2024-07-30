FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3214", "main:app"]
