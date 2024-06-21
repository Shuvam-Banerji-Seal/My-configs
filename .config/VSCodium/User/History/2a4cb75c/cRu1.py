import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the step function
def step_function(x):
    return np.where(x < 0, -1, 1)

# Fourier series approximation
def fourier_series_approximation(x, n_terms):
    approximation = np.zeros_like(x)
    for n in range(1, n_terms + 1, 2):
        approximation += (4 / (np.pi * n)) * np.sin(n * x)
    return approximation

# Setup the plot
fig, ax = plt.subplots()
x = np.linspace(-np.pi, np.pi, 1000)
y = step_function(x)
line, = ax.plot(x, y, label='Step Function')
approx_line, = ax.plot([], [], label='Fourier Series Approximation', color='red')
ax.legend()

# Initialize the plot
def init():
    approx_line.set_data([], [])
    return approx_line,

# Update function for animation
def update(n_terms):
    y_approx = fourier_series_approximation(x, n_terms)
    approx_line.set_data(x, y_approx)
    ax.set_title(f'Fourier Series Approximation with {n_terms} Terms')
    return approx_line,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=range(1, 510, 2), init_func=init, blit=True, repeat=False)

# Display the animation
plt.show()
