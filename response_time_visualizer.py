import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV files
df1 = pd.read_csv('response_config_1_yaml.csv', header=None, names=['time1'])
df2 = pd.read_csv('response_config_2_yaml.csv', header=None, names=['time2'])

response_times1 = df1['time1'].values
response_times2 = df2['time2'].values

light_blue = '#87CEEB'  # Light blue color
dark_blue = '#1E90FF'   # Dark blue color

# Create histogram plots
plt.hist(response_times1, bins=50, alpha=0.8, color=light_blue, label='Same Host Response Time', edgecolor='black', linewidth=1.2)
plt.hist(response_times2, bins=50, alpha=0.8, color=dark_blue, label='Different Host Response Time', edgecolor='black', linewidth=1.2)

# Add labels and a title
plt.xlabel('Response Time (ms)')
plt.ylabel('Frequency')
plt.title('Response Time Histogram (Comparison)')

# Add a legend
plt.legend(loc='upper right')

# Save the plot as an image (PNG)
plt.savefig('configuration-comparison-results.png')

# Show the plot
plt.show()
