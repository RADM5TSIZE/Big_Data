FROM python:3.8.10
RUN mkdir /webapp
WORKDIR /webapp
ADD . /webapp/
RUN pip install -r requirements.txt
#pymemcache does not work when inside requirements.txt
RUN pip install pymemcache
EXPOSE 5000
CMD ["python", "/webapp/app.py"]
