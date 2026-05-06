FROM python:3.11-slim
 
WORKDIR /app
 
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . .
 
EXPOSE 8002
 
CMD sh -c "until python manage.py migrate --run-syncdb 2>/dev/null; do echo 'Esperando MySQL...'; sleep 3; done && python manage.py runserver 0.0.0.0:8002"
 
