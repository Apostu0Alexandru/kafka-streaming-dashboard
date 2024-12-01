from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time
import random
import logging
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_sensor_data():
    return {
        'timestamp': int(time.time()),
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 60.0), 2),
        'pressure': round(random.uniform(990.0, 1010.0), 2)
    }

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def create_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=json_serializer
    )

producer = create_producer()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def send_data(data):
    future = producer.send('sensor_data', data)
    record_metadata = future.get(timeout=10)
    logging.info(f"Sent: {data} to partition {record_metadata.partition} at offset {record_metadata.offset}")

if __name__ == "__main__":
    while True:
        try:
            sensor_data = generate_sensor_data()
            logging.info(f"Generated sensor data: {sensor_data}")
            send_data(sensor_data)
            time.sleep(1)
        except KafkaError as e:
            logging.error(f"Failed to send message: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            break

    producer.close()