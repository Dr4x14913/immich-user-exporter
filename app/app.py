from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CollectorRegistry
import requests
import os
from datetime import datetime

# Configuration
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

# Flask App
app = Flask(__name__)

# Prometheus Registry
registry = CollectorRegistry()

# Prometheus Metrics
photos_gauge = Gauge('user_photos', 'Number of photos per user', ['user_name'], registry=registry)
videos_gauge = Gauge('user_videos', 'Number of videos per user', ['user_name'], registry=registry)
usage_gauge = Gauge('user_usage_bytes', 'Storage usage per user in bytes', ['user_name'], registry=registry)
quota_gauge = Gauge('user_quota_bytes', 'Storage quota per user in bytes', ['user_name'], registry=registry)

def fetch_data():
    """Fetch data from the Immich API."""
    try:
        response = requests.get(
            API_URL,
            headers={
                'Accept': 'application/json',
                'x-api-key': API_KEY
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def update_metrics():
    """Update Prometheus metrics with the latest data."""
    data = fetch_data()
    if data and 'usageByUser' in data:
        for user in data['usageByUser']:
            user_name = user.get('userName', 'unknown')
            photos_gauge.labels(user_name=user_name).set(user.get('photos', 0))
            videos_gauge.labels(user_name=user_name).set(user.get('videos', 0))
            usage_gauge.labels(user_name=user_name).set(user.get('usage', 0))
            quota_gauge.labels(user_name=user_name).set(user.get('quotaSizeInBytes', 0) or 0)
#
@app.route("/")
def current_time():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time: {formatted_time}"

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    print("gfgg", flush=True)
    update_metrics()
    return Response(generate_latest(registry), mimetype='text/plain')

if __name__ == '__main__':
    print("jj", flush=True)
    app.run(host='0.0.0.0', debug=True, port=8050)

