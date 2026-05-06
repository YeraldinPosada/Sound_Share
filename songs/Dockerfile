FROM python:3.12-slim

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

CMD sh -c "until python -c \"import MySQLdb; MySQLdb.connect(host='mysql', user='soundshare', passwd='1234', db='songs')\" 2>/dev/null; do echo 'Esperando MySQL...'; sleep 3; done && python mi_api/manage.py migrate && python mi_api/manage.py runserver 0.0.0.0:8002"
