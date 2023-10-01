import requests
import time
import csv
import sys


config_name: str = str(sys.argv[1])
host_name: str = str(sys.argv[2])
node_app_url = f"http://{host_name}:1717"
num_requests = 30
response_times = []

print(f"Collecting response time for configuration -> {config_name}")

# Send requests and record response times
for _ in range(num_requests):
    start_time = time.time()
    response = requests.get(node_app_url)
    end_time = time.time()

    # Calculate response time in milliseconds
    response_time_ms = (end_time - start_time) * 1000
    print(f"Response Time for sequence call {_} -> {response_time_ms} ms")

    response_times.append(response_time_ms)

# Overwrite the CSV file with new response times
with open(f'response_{config_name}_yaml.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for response_time_ms in response_times:
        csv_writer.writerow([response_time_ms])

# Calculate total time
total_time = sum(response_times)

# Overwrite the text file with the total time
with open(f'total_time_taken_{config_name}.txt', 'w') as txt_file:
    txt_file.write(f"Total_Time\n{total_time}\n")
