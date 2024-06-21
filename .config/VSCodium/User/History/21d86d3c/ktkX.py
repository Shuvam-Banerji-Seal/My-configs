import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import sparse
from scipy.sparse.linalg import spsolve

# Function to load data from the file
def load_data(filename):
    data = pd.read_csv(filename, delimiter='\t', skiprows=3)
    return data

# Function to renormalize y values
def renormalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

# Function to apply baseline correction using Savitzky-Golay filter
def baseline_correction_savgol(y_data, window_length=101, polyorder=2):
    baseline = savgol_filter(y_data, window_length, polyorder)
    corrected = y_data - baseline
    return corrected

# Function to apply baseline correction using Asymmetric Least Squares
def baseline_correction_als(y_data, lam=1e6, p=0.01, niter=10):
    L = len(y_data)
    D = sparse.diags([1, -2, 1], [0, 1, 2], shape=(L, L - 2))
    D = lam * D.dot(D.transpose())
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + D
        z = spsolve(Z, w * y_data)
        w = p * (y_data > z) + (1 - p) * (y_data < z)
    corrected = y_data - z
    return corrected

# Load the data
filename = '/home/shuvam/Codes/Random/CUw12.txt'
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

# Apply baseline correction using Savitzky-Golay filter
y_corrected_savgol = baseline_correction_savgol(y_normalized)

# Apply baseline correction using Asymmetric Least Squares
y_corrected_als = baseline_correction_als(y_normalized)

# Plot original, normalized, and corrected data
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(x_selected, y_selected, label='Original Data')
plt.xlabel('Time')
plt.ylabel('Intensity')
plt.title('Original Data')
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(x_selected, y_normalized, label='Normalized Data', color='orange')
plt.xlabel('Time')
plt.ylabel('Normalized Intensity')
plt.title('Normalized Data')
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(x_selected, y_corrected_savgol, label='Baseline Corrected Data (Savgol)', color='green')
plt.xlabel('Time')
plt.ylabel('Corrected Intensity')
plt.title('Baseline Corrected Data (Savgol)')
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(x_selected, y_corrected_als, label='Baseline Corrected Data (ALS)', color='blue')
plt.xlabel('Time')
plt.ylabel('Corrected Intensity')
plt.title('Baseline Corrected Data (ALS)')
plt.legend()

plt.tight_layout()
plt.show()
