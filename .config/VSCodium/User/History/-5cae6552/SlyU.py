import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the step function
def step_function(x):
    return np.where(x < 0, -1, 7)

# Number of sample points
N = 256
# Sample spacing
T = 2 * np.pi / N

# Discrete sample points
x = np.linspace(-np.pi, np.pi, N)
y = step_function(x)

# Fourier transform of the step function
yf = np.fft.fft(y)
xf = np.fft.fftfreq(N, T)

# Setup the plot
fig, ax = plt.subplots()
line, = ax.plot(x, y, label='Original Step Function')
approx_line, = ax.plot([], [], label='Fourier Transform Approximation', color='red')
ax.legend()
ax.set_ylim(-1.5, 1.5)

# Initialize the plot
def init():
    approx_line.set_data([], [])
    return approx_line,

# Update function for animation
def update(n_terms):
    # Reconstruct the signal using inverse FFT with n_terms
    yf_filtered = np.zeros_like(yf)
    yf_filtered[:n_terms] = yf[:n_terms]
    yf_filtered[-n_terms:] = yf[-n_terms:]
    y_approx = np.fft.ifft(yf_filtered)
    approx_line.set_data(x, y_approx.real)
    ax.set_title(f'Fourier Transform Approximation with {n_terms} Terms')
    return approx_line,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=range(1, N//2, 2), init_func=init, blit=True, repeat=False)

# Display the animation
plt.show()
