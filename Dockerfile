FROM python:3.9-alpine

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

RUN python setup.py install