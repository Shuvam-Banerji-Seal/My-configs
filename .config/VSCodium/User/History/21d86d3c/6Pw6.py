import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Function to load data from the file
def load_data(filename):
    data = pd.read_csv(filename, delimiter='\t', skiprows=3, names=["Time", "Intensity"])
    return data

# Function to renormalize y values
def renormalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

# Function to apply baseline correction using Savitzky-Golay filter
def baseline_correction(y_data, window_length=101, polyorder=2):
    baseline = savgol_filter(y_data, window_length, polyorder)
    corrected = y_data - baseline
    return corrected

# Load the data
filename = '/mnt/data/CUw12.txt'
data = load_data(filename)

# Prompt user for x-range
start_time = float(input("Enter start time for x-range: "))
end_time = float(input("Enter end time for x-range: "))

# Select data within the x-range
selected_data = data[(data['Time'] >= start_time) & (data['Time'] <= end_time)]
x_selected = selected_data['Time'].values
y_selected = selected_data['Intensity'].values

# Renormalize the y-axis data points
y_normalized = renormalize(y_selected)

# Apply baseline correction
y_corrected = baseline_correction(y_normalized)

# Plot original, normalized, and corrected data
plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.plot(x_selected, y_selected, label='Original Data')
plt.xlabel('Time')
plt.ylabel('Intensity')
plt.title('Original Data')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(x_selected, y_normalized, label='Normalized Data', color='orange')
plt.xlabel('Time')
plt.ylabel('Normalized Intensity')
plt.title('Normalized Data')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(x_selected, y_corrected, label='Baseline Corrected Data', color='green')
plt.xlabel('Time')
plt.ylabel('Corrected Intensity')
plt.title('Baseline Corrected Data')
plt.legend()

plt.tight_layout()
plt.show()
