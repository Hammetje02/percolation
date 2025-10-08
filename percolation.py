import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Grid size
N = 100

# Probability that a site is open
p = 0.6  # You can change this value between 0 and 1

# Initialize grid (all blocked initially)
grid = np.zeros((N, N), dtype=int)  # 0 = blocked, 1 = open

# Function to check percolation using DFS
def percolates(grid):
    visited = np.zeros_like(grid, dtype=bool)
    
    def dfs(x, y):
        if x < 0 or x >= N or y < 0 or y >= N:
            return False
        if not grid[x, y] or visited[x, y]:
            return False
        visited[x, y] = True
        if x == N-1:
            return True
        return (dfs(x+1, y) or dfs(x-1, y) or dfs(x, y+1) or dfs(x, y-1))
    
    for col in range(N):
        if grid[0, col] and dfs(0, col):
            return True
    return False

# Setup matplotlib figure
fig, ax = plt.subplots()
im = ax.imshow(grid, cmap='Greys', vmin=0, vmax=1)
ax.set_title(f"Percolation Simulation (p={p})")

def update(frame):
    global grid
    # Randomly open a site based on probability p
    for _ in range(N):  # Open N sites per frame for speed
        x, y = random.randint(0, N-1), random.randint(0, N-1)
        if random.random() < p:
            grid[x, y] = 1

    im.set_data(grid)

    if percolates(grid):
        ax.set_title(f"The system percolates! (p={p})")
    else:
        ax.set_title(f"Percolation Simulation (p={p})")
    return [im]

ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=True)
plt.show()
