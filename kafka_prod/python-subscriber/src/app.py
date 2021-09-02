# Install: pip3 install kafka-python
from kafka import KafkaConsumer

# The bootstrap server to connect to
bootstrap = 'my-cluster-kafka-bootstrap:9092'

# Create a comsumer instance
# cf.
print('Starting KafkaConsumer')
consumer = KafkaConsumer('big_data_demo',  # <-- topics
                         bootstrap_servers=bootstrap)

# Print out all received messages
for msg in consumer:
    print("Message Received: ", msg)
