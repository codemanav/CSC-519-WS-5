from flask import Flask, jsonify
import redis
import time
import json
import math
import requests
import os

app = Flask(__name__)
redis_pass = os.environ.get("REDIS_PASS", "default_password")
ip = os.environ.get("IP_HOST", "default_password")

# Initialize Redis client
client = redis.Redis(host='127.0.0.1', port=6379, password=redis_pass)

# Initialize tracking lists
random_points = []
closest_points = []
distances = []
api_elapsed_times = []
local_elapsed_times = []


# Utility function to calculate Cartesian distance
def cartesian_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

@app.route('/generate_data', methods=['GET'])
def generate_data():
    for i in range(30):
        # Simulated API call
        start_time = time.time()
        response = requests.get('http://' + ip)
        end_time = time.time()
        data = response.json()
        elapsed_time = (end_time - start_time) * 1000
        api_elapsed_times.append(elapsed_time)

        # Local nearest neighbor search
        local_start_time = time.time()
        find_closest_point_local(data['random_point']['x'], data['random_point']['y'])
        local_end_time = time.time()
        local_elapsed_time = (local_end_time - local_start_time) * 1000
        print(local_elapsed_time)
        local_elapsed_times.append(local_elapsed_time)

    # Save times to a file
    save_data()
    return jsonify({"message": "Data generated successfully"})

@app.route('/api/data', methods=['GET'])
def get_data():
    if len(api_elapsed_times) == 30 and len(local_elapsed_times) == 30:
        data = {
            'api_elapsed_times': api_elapsed_times,
            'local_elapsed_times': local_elapsed_times,
            'random_points': random_points,
            'closest_points': closest_points,
            'distances': distances
        }
        return jsonify(data)
    else:
        return jsonify({'message': 'Data is still being generated. Please check back later.'})


def find_closest_point_local(x_rand, y_rand):
    closest_point = None
    min_distance = float('inf')
    cursor = '0'

    while cursor != '0':
        cursor, keys = client.scan(cursor, match='point:*')
        for key in keys:
            point_json = client.get(key)
            point = json.loads(point_json.decode('utf-8'))
            x = point['x']
            y = point['y']
            distance = cartesian_distance(x_rand, y_rand, x, y)
            if distance < min_distance:
                min_distance = distance
                closest_point = point

    return closest_point

def save_data():
    with open('/var/www/db_file/elapsedTimesAPI.json', 'w') as api_file:
        json.dump(api_elapsed_times, api_file)

    with open('/var/www/db_file/elapsedTimesLocal.json', 'w') as local_file:
        json.dump(local_elapsed_times, local_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
