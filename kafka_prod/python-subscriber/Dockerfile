FROM python:3-alpine

RUN pip install --upgrade pip

RUN adduser -D python
USER python
WORKDIR /home/python

COPY --chown=python:python requirements.txt .
ENV PATH="/home/python/.local/bin:${PATH}"
RUN pip install --user -r requirements.txt

COPY --chown=python:python src src

CMD ["python", "/home/python/src/app.py"]
