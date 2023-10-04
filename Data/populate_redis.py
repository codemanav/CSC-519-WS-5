import csv
import redis
import os
import json
import time

def connect_to_redis():
    while True:
        try:
            r = redis.Redis(host='localhost', port=6379, db=0, password=redis_pass)
            if r.ping():  # Check if the instance is actually connected
                return r
        except redis.ConnectionError:
            print("Failed to connect to Redis. Retrying in 5 seconds.")
            time.sleep(5)

# Set up Redis connection
redis_pass = os.environ.get("REDIS_PASS", "default_password")
r = connect_to_redis()
r.flushdb()

# Read the CSV file and populate Redis
with open('/var/www/db_file/rand-x-y-data.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for i, row in enumerate(csvreader):
        if i == 0:  # skip header row
            continue
        x = float(row[0])  # x
        y = float(row[1])  # y

        # Construct a JSON object for the point
        point = {
            'x': x,
            'y': y
        }

        # Convert the point to JSON string
        point_json = json.dumps(point)

        try:
            # Add the point to Redis with key as 'point:{index}'
            r.set(f'point:{i}', point_json)
        except (redis.ConnectionError, redis.TimeoutError):
            print("Lost connection to Redis. Reconnecting...")
            r = connect_to_redis()
