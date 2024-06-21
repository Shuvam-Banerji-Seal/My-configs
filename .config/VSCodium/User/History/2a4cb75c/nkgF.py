import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import square

# Function to calculate the Fourier series coefficients
def fourier_coefficients(n, T, duty_cycle):
    coefficients = []
    for i in range(1, n+1):
        if i % 2 != 0:
            coefficients.append((2/(i*np.pi)) * (1 - np.cos(2*np.pi*i*duty_cycle/T)))
        else:
            coefficients.append(0)
    return coefficients

# Function to calculate the Fourier series approximation
def fourier_series(x, n, T, duty_cycle):
    series = np.zeros_like(x)
    coefficients = fourier_coefficients(n, T, duty_cycle)
    for i in range(len(coefficients)):
        series += coefficients[i] * np.sin(2*np.pi*(i+1)*x/T)
    return series

# Step function
def step_function(x, T, duty_cycle):
    return np.where((x % T) < (T * duty_cycle), 1, 0)

# Parameters
T = 2*np.pi  # Period of the step function
duty_cycle = 0.5  # Duty cycle of the step function
n_terms = 10  # Number of terms in the Fourier series
frames = 200  # Number of frames in the animation

# Generate x values
x = np.linspace(0, 4*np.pi, 1000)

# Create a figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 4*np.pi)
ax.set_ylim(-0.5, 1.5)

# Initialize line objects
step_line, = ax.plot([], [], label='Step Function')
fourier_line, = ax.plot([], [], label='Fourier Series Approximation')

# Function to update the plot for each frame
def update(frame):
    step_line.set_data(x, step_function(x + frame*np.pi/frames, T, duty_cycle))
    fourier_line.set_data(x, fourier_series(x, n_terms, T, duty_cycle))
    return step_line, fourier_line

# Create the animation
ani = FuncAnimation(fig, update, frames=frames, blit=True)

# Show the plot
plt.legend()
plt.show()
