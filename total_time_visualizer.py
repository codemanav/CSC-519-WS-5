import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv('total_time_taken_config_1.txt', header=None, names=['time1'])
df2 = pd.read_csv('total_time_taken_config_2.txt', header=None, names=['time2'])

response_times1 = df1['time1'].values
response_times2 = df2['time2'].values

plt.hist(response_times1, bins=10, alpha=0.8, color='blue', label='Same Host Total Time Taken')
plt.hist(response_times2, bins=10, alpha=0.8, color='red', label='Different Host Total Time Taken')

# Add labels and a title
plt.xlabel('Response Time (ms)')
plt.ylabel('Frequency')
plt.title('Response Time Histogram (Comparison)')

# Add a legend
plt.legend(loc='upper right')

# Show the combined histogram
plt.show()

plt.savefig('configuration-comparison-results.png')




