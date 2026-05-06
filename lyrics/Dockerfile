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

EXPOSE 5001

CMD sh -c "until python -c \"import pymysql; pymysql.connect(host='mysql', user='soundshare', password='1234', database='lyrics')\" 2>/dev/null; do echo 'Esperando MySQL...'; sleep 3; done && flask db upgrade && python app.py"