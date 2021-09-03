import time
from essential_generators import DocumentGenerator
from kafka import KafkaProducer
import time
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('mysql+pymysql://root:root@my-app-mysql-service:3306/crimes', connect_args={'connect_timeout':120}, pool_pre_ping=True)

crimes = pd.read_sql('Chicago_Crimes_sample', con=engine.connect())



time.sleep(40)
gen = DocumentGenerator()
print("Gestartet")
producer = KafkaProducer(
    bootstrap_servers='my-cluster-kafka-bootstrap:9092')
print("Verbindung hergestellt")
while True:

    sample = crimes.sample(n=1)
    json = sample.to_json()
  
    next_msg = json   
    
    print(f"Sending message: {next_msg}")
    future = producer.send("big_data_demo", next_msg.encode())
    result = future.get(timeout=5)
    print(f"Result: {result}")
    time.sleep(30)
