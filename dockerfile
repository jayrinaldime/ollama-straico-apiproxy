FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3214

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3214"]
