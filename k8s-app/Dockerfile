FROM python:3.8.10
EXPOSE 5000
RUN mkdir /webapp
WORKDIR /webapp
ADD . /webapp/
RUN pip install -r requirements.txt

CMD ["python", "/webapp/app_mit_memcache.py"]
