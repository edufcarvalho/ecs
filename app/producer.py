from app import KafkaProducer
import json
import time

# Setup Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to generate data
def produce(data):
    producer.send('emotions', value=data)
    print(f"Sent: {data}")

if __name__ == "__main__":
    test_data = [] # insert here data to test
    
    for data in test_data:
        produce(data)

    # Closing producer
    producer.flush()
    producer.close()