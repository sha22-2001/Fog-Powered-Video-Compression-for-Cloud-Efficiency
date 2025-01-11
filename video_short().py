import matplotlib.pyplot as plt
import numpy as np

# Function to generate O(N + M) time complexity
def complexity_N_M(N, M):
    return N + M

# Function to generate O(W * H) time complexity
def complexity_W_H(W, H):
    return W * H

# Generate data points
N_values = np.arange(1, 100, 5)  # Vary N from 1 to 100 with step 5
M_values = np.arange(1, 100, 5)  # Vary M from 1 to 100 with step 5

W_values = np.arange(1, 100, 5)  # Vary W from 1 to 100 with step 5
H_values = np.arange(1, 100, 5)  # Vary H from 1 to 100 with step 5

# Calculate time complexities
N_M_complexity = complexity_N_M(N_values, M_values)
W_H_complexity = complexity_W_H(W_values, H_values)

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(N_values, N_M_complexity, label='O(N + M) - Clip merge')
plt.plot(W_values, W_H_complexity, label='O(W * H) - sliding window')
plt.xlabel('Input Size')
plt.ylabel('Time Complexity')
plt.title('Time Complexity Comparison')
plt.legend()
plt.grid(True)

# Save the graph
num_images = 1  # Update the number of images accordingly
plt.savefig(f"Graph/{num_images}.png")  # Save in the specified directory

plt.show()
