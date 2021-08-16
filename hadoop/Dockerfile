FROM python:3.8.10

RUN mkdir /hadoop

WORKDIR /hadoop

ADD . /hadoop/

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "/hadoop/hdfs.py"]
