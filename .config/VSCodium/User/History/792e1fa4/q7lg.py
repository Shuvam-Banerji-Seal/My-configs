import time
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def compute_mandelbrot_segment(segment):
    (xmin, xmax, ymin, ymax, width, height, max_iter, start, end) = segment
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((end - start, height))

    for i in range(start, end):
        for j in range(height):
            n3[i - start, j] = mandelbrot(r1[i] + 1j*r2[j], max_iter)

    return n3

def compute_mandelbrot_parallel(xmin, xmax, ymin, ymax, width, height, max_iter, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    segment_size = (width + num_processes - 1) // num_processes  # Distribute remainder evenly
    segments = [(xmin, xmax, ymin, ymax, width, height, max_iter, i * segment_size, min((i + 1) * segment_size, width)) for i in range(num_processes)]

    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(compute_mandelbrot_segment, segments)
    pool.close()
    pool.join()

    n3 = np.vstack(results)
    return n3

def compute_mandelbrot_single_threaded(xmin, xmax, ymin, ymax, width, height, max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))

    for i in range(width):
        for j in range(height):
            n3[i, j] = mandelbrot(r1[i] + 1j*r2[j], max_iter)

    return n3

if __name__ == "__main__":
    xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
    width, height = 1000, 1000
    max_iter = 256
    num_processes = multiprocessing.cpu_count()

    # Single-threaded version
    start_time = time.time()
    result = compute_mandelbrot_single_threaded(xmin, xmax, ymin, ymax, width, height, max_iter)
    end_time = time.time()
    print(f"Time taken (single-threaded): {end_time - start_time} seconds")

    plt.imshow(result.T, extent=[xmin, xmax, ymin, ymax], cmap='hot')
    plt.colorbar()
    plt.title("Mandelbrot Set (Single-threaded)")
    plt.show()

    # Multi-threaded version
    start_time = time.time()
    result_parallel = compute_mandelbrot_parallel(xmin, xmax, ymin, ymax, width, height, max_iter, num_processes)
    end_time = time.time()
    print(f"Time taken (multi-threaded): {end_time - start_time} seconds")

    plt.imshow(result_parallel.T, extent=[xmin, xmax, ymin, ymax], cmap='hot')
    plt.colorbar()
    plt.title("Mandelbrot Set (Multi-threaded)")
    plt.show()