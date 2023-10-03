import requests
import time
import matplotlib.pyplot as plt

import yaml

file_path = r'C:\Users\psvka\OneDrive\Desktop\fall23\CSC519\CSC-519-WS-5\vars.yaml'
with open(file_path, 'r') as file:
    data = yaml.safe_load(file)
#print(data)
host_1 = data['db_host']        # 1-Configuration
host_2 = data['app_user_host']  #2-Configuration
time_1 = []
time_2 = []

start_time = time.time()
for i in range(30):
    response = requests.get(f'http://{host_1}')
    time_1.append(response.elapsed.total_seconds()*1000)
end_time = time.time()
total_time_1 = (end_time - start_time)*1000
#time_1.append(total_time_1)
print('For Configuration-1')
for i in range(len(time_1)):
    print(f'{i+1}th request took {time_1[i]} milliseconds')



print(f'Total time taken by to complete 30 queries on Configuration-1 : {total_time_1} milliseconds')
print('*************************************************************')
start_time = time.time()
for i in range(30):
    response = requests.get(f'http://{host_2}')
    time_2.append(response.elapsed.total_seconds()*1000)
end_time = time.time()
total_time_2 = (end_time - start_time)*1000
#time_2.append(total_time_2)
print('For Configuration-2')
for i in range(len(time_1)):
    print(f'{i+1}th request took {time_2[i]} milliseconds')



print(f'Total time taken by to complete 30 queries on Configuration-2 : {total_time_2} milliseconds')


plt.hist(time_1, alpha=0.6, color='blue', label='1-configuration')
plt.hist(time_2, alpha=0.6, color='g', label='2-configuration')
plt.xlabel('Time in milliseconds')
plt.ylabel('Counts')
plt.legend()
plt.show()