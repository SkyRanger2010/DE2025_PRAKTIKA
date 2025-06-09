FROM python:3.9-slim

WORKDIR /app
RUN mkdir -p /app/data && chmod 777 /app/data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /app/data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]