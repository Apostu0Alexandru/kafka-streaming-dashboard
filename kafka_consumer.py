from kafka import KafkaConsumer
import json
import logging
import sqlite3
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

consumer = KafkaConsumer(
    'sensor_data',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Database setup
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_readings (
        timestamp INTEGER,
        temperature REAL,
        humidity REAL,
        pressure REAL
    )
''')
conn.commit()

def insert_data(data):
    cursor.execute('''
        INSERT INTO sensor_readings (timestamp, temperature, humidity, pressure)
        VALUES (?, ?, ?, ?)
    ''', (data['timestamp'], data['temperature'], data['humidity'], data['pressure']))
    conn.commit()
    logging.info(f"Inserted data into database: {data}")

if __name__ == "__main__":
    try:
        for message in consumer:
            data = message.value
            logging.info(f"Received: {data}")
            insert_data(data)
    except KeyboardInterrupt:
        logging.info("Consumer stopped by user")
    finally:
        consumer.close()
        conn.close()