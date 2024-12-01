from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import time
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_latest_data():
    try:
        conn = sqlite3.connect('sensor_data.db')
        five_minutes_ago = int(time.time()) - 300
        query = f"""
        SELECT * FROM sensor_readings 
        WHERE timestamp > {five_minutes_ago}
        ORDER BY timestamp DESC 
        LIMIT 60
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        logging.info(f"Retrieved {len(df)} rows from database")
        return df
    except Exception as e:
        logging.error(f"Error retrieving data from database: {e}")
        return pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    df = get_latest_data()
    if df.empty:
        logging.warning("No data retrieved from database")
        return jsonify({
            'timestamps': [],
            'temperatures': [],
            'humidities': [],
            'pressures': [],
            'current_time': int(time.time())
        })
    
    timestamps = [datetime.fromtimestamp(ts).strftime('%H:%M:%S') for ts in df['timestamp']]
    
    response_data = {
        'timestamps': timestamps,
        'temperatures': df['temperature'].tolist(),
        'humidities': df['humidity'].tolist(),
        'pressures': df['pressure'].tolist(),
        'current_time': int(time.time())
    }
    logging.info(f"Sending data: {response_data}")
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)