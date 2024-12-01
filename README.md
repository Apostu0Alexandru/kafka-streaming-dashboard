

```markdown
# Kafka Streaming Dashboard

## Overview

This project implements a real-time data streaming pipeline using Apache Kafka, with a web-based dashboard for visualization. It simulates sensor data, processes it through a Kafka pipeline, stores it in a SQLite database, and displays it in real-time on a web dashboard.

## Components

- `kafka_producer.py`: Simulates sensor data (temperature, humidity, pressure) and sends it to a Kafka topic.
- `kafka_consumer.py`: Consumes data from Kafka, processes it, and stores it in a SQLite database.
- `app.py`: Flask web application that serves the dashboard and provides API endpoints for real-time data.
- `templates/index.html`: Frontend for the dashboard, using Plotly.js for real-time charts.

## Prerequisites

- Python 3.7+
- Apache Kafka 2.8+
- SQLite 3

## Installation

1. Clone the repository:
```

git clone [https://github.com/Apostu0Alexandru/kafka-streaming-dashboard.git](https://github.com/Apostu0Alexandru/kafka-streaming-dashboard.git)
cd kafka-streaming-dashboard

```plaintext

2. Create and activate a virtual environment:
```

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

```plaintext

3. Install dependencies:
```

pip install -r requirements.txt

```plaintext

## Configuration

1. Ensure Kafka is installed and running on your system. If not, follow the [official Kafka quickstart guide](https://kafka.apache.org/quickstart).

2. Create a Kafka topic named 'sensor_data':
```

kafka-topics.sh --create --topic sensor_data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

```plaintext

3. If needed, adjust the Kafka broker address in `kafka_producer.py` and `kafka_consumer.py`:
```python
bootstrap_servers=['localhost:9092']
```

## Usage

1. Start the Kafka producer to simulate sensor data:

```plaintext
python kafka_producer.py
```


2. In a new terminal, start the Kafka consumer to process and store data:

```plaintext
python kafka_consumer.py
```


3. In another terminal, start the Flask web application:

```plaintext
python app.py
```


4. Open a web browser and navigate to `http://localhost:5000` to view the real-time dashboard.


## Project Structure

```plaintext
kafka-streaming-project/
├── kafka_producer.py
├── kafka_consumer.py
├── app.py
├── templates/
│   └── index.html
├── requirements.txt
├── README.md
└── .gitignore
```

## Data Flow

1. The Kafka producer generates simulated sensor data and sends it to the 'sensor_data' Kafka topic.
2. The Kafka consumer reads from the 'sensor_data' topic and stores the data in a SQLite database.
3. The Flask application queries the SQLite database and serves the data through an API.
4. The frontend (index.html) fetches data from the API and updates the charts in real-time.


## Troubleshooting

- If you encounter `NoBrokersAvailable` error, ensure that Kafka is running and the broker address is correct.
- If the dashboard is not updating, check the browser console for any JavaScript errors and the Flask application logs for backend issues.
- For database-related issues, you can use the SQLite command-line tool to inspect the database:

```plaintext
sqlite3 sensor_data.db
```




## Contributing

Contributions to this project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Apache Kafka for providing a robust distributed streaming platform.
- Flask for the web application framework.
- Plotly.js for the interactive charts.


## Note

This project is for demonstration purposes and may require additional configuration and security measures for production use.

