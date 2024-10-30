import matplotlib.pyplot as plt
import numpy as np

# Generate some sample data (e.g., daily temperatures)
temperatures = np.random.normal(loc=25, scale=5, size=1000)  # 1000 data points, mean=25°C, std dev=5°C

# Create the histogram
plt.figure(figsize=(10, 6))
plt.hist(temperatures, bins=30, color='skyblue', edgecolor='black')
plt.title('Temperature Distribution Over 1000 Days')
plt.xlabel('Temperature (°C)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
