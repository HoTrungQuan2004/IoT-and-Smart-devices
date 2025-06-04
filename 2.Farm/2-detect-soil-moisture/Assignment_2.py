import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample data
data = {
    'sample': ['A', 'B', 'C'],
    'wet_weight': [212, 245, 180],
    'dry_weight': [197, 210, 160],
    'sensor_reading': [620, 710, 580]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate Gravimetric Moisture %
df['moisture_percent'] = ((df['wet_weight'] - df['dry_weight']) / df['dry_weight']) * 100

# Print results
print(df[['sample', 'sensor_reading', 'moisture_percent']])

# Plot
plt.figure(figsize=(8, 5))
plt.scatter(df['sensor_reading'], df['moisture_percent'], color='blue', label='Samples')
plt.title('Soil Moisture % vs. Sensor Reading')
plt.xlabel('Sensor Reading')
plt.ylabel('Soil Moisture (%)')
plt.grid(True)

# Fit and plot trend line (linear)
z = np.polyfit(df['sensor_reading'], df['moisture_percent'], 1)
p = np.poly1d(z)
plt.plot(df['sensor_reading'], p(df['sensor_reading']), "--r", label='Best Fit Line')
plt.legend()
plt.tight_layout()
plt.show()
