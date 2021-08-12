FROM python:3.8.10
RUN mkdir /webapp
WORKDIR /webapp
ADD . /webapp/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/webapp/app.py"]
