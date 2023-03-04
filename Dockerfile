FROM python:3.9.12

RUN mkdir wd
WORKDIR wd
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . ./
 
CMD []
