import matplotlib.pyplot as plt
import numpy as np
import time


def algorithm_n_squared(data):
    start_time = time.time()
    # Algorithm with O(n^2) complexity
    for _ in range(len(data)):
        for _ in range(len(data)):
            pass
    return time.time() - start_time


def algorithm_n(data):
    start_time = time.time()
    # Algorithm with O(n) complexity
    for _ in range(len(data)):
        pass
    return time.time() - start_time


# Define the range of input sizes
input_sizes = np.arange(1, 1001, 50)  # Adjust the range as needed

# Initialize lists to store execution times
execution_times_n_squared = []
execution_times_n = []

for size in input_sizes:
    # Generate synthetic data of the specified size
    data = list(range(size))

    # Measure execution time for O(n^2) algorithm
    time_n_squared = algorithm_n_squared(data)
    execution_times_n_squared.append(time_n_squared)

    # Measure execution time for O(n) algorithm
    time_n = algorithm_n(data)
    execution_times_n.append(time_n)

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(input_sizes, execution_times_n_squared, color='orange', label='O(n^2) - Sliding Window')
plt.plot(input_sizes, execution_times_n, color='dodgerblue', label='O(1) - Clip merge')
plt.xlabel('Input Size')
plt.ylabel('Frame rate (s)')
plt.title('Comparison of Size taken per frame')
plt.legend()
plt.grid(True)

# Save the graph
num_images = 1  # Update the number of images accordingly
plt.savefig(f"Graph/{num_images}-Conf.png")  # Save in the specified directory

plt.show()
