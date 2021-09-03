FROM python:3-slim

RUN pip install --upgrade pip

#RUN adduser -D python
#USER python
WORKDIR /work

COPY requirements.txt .
#ENV PATH="/home/python/.local/bin:${PATH}"
RUN pip install -r requirements.txt

COPY src/ /src

#RUN tree /

CMD ["python", "/src/app.py"]
