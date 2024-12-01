import unittest
from unittest.mock import patch
from kafka_producer import generate_sensor_data, json_serializer

class TestKafkaProducer(unittest.TestCase):

    def test_generate_sensor_data(self):
        data = generate_sensor_data()
        self.assertIn('timestamp', data)
        self.assertIn('temperature', data)
        self.assertIn('humidity', data)
        self.assertIn('pressure', data)
        self.assertTrue(20 <= data['temperature'] <= 30)
        self.assertTrue(30 <= data['humidity'] <= 60)
        self.assertTrue(990 <= data['pressure'] <= 1010)

    def test_json_serializer(self):
        data = {'test': 'data'}
        serialized = json_serializer(data)
        self.assertIsInstance(serialized, bytes)
        self.assertEqual(serialized, b'{"test": "data"}')

    @patch('kafka_producer.KafkaProducer')
    def test_create_producer(self, mock_kafka_producer):
        from kafka_producer import create_producer
        producer = create_producer()
        mock_kafka_producer.assert_called_once_with(
            bootstrap_servers=['localhost:9092'],
            value_serializer=json_serializer
        )

if __name__ == '__main__':
    unittest.main()