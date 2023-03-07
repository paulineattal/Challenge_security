FROM python:latest

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
 
CMD ["gunicorn", "-b 0.0.0.0:80", "index:server"]