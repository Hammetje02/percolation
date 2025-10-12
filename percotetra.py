import numpy as np
import matplotlib.pyplot as plt
from collections import deque

N = 100
np.random.seed(13)
p = 0.6  # around percolation threshold

# 0 = open, 1 = blocked
grid = np.where(np.random.random([N, N]) < p, 0, 1)

visited = np.zeros((N, N))
path2 = np.zeros((N, N))
found_path = False


def bfs_percolate(start_positions, direction="vertical"):
    """Iterative BFS to find percolating path (tetra-shape connectivity)."""
    global visited, path2, found_path
    queue = deque()
    parent = {}  # store parent for path reconstruction

    for pos in start_positions:
        x, y = pos
        if grid[x, y] == 0:
            queue.append((x, y))
            visited[x, y] = 1

    # Define tetra-shape neighbors
    neighbor_offsets = [
        (1, 1), (1, -1), (-1, 1), (-1, -1),  # diagonals
        (2, 0), (-2, 0)                      # two-step vertical
    ]

    while queue:
        x, y = queue.popleft()

        # Check percolation condition
        if direction == "vertical" and x == N - 1:
            found_path = True
            reconstruct_path((x, y), parent)
            print("Vertical percolation found!")
            return True
        elif direction == "horizontal" and y == N - 1:
            found_path = True
            reconstruct_path((x, y), parent)
            print("Horizontal percolation found!")
            return True

        # Explore tetra neighbors
        for dx, dy in neighbor_offsets:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and grid[nx, ny] == 0 and visited[nx, ny] == 0:
                visited[nx, ny] = 1
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return False


def reconstruct_path(end, parent):
    """Rebuild the path from end to start using parent dictionary."""
    global path2
    x, y = end
    while (x, y) in parent:
        path2[x, y] = 1
        x, y = parent[(x, y)]
    path2[x, y] = 1  # include start


def finding_cluster():
    global found_path

    # Try top-to-bottom percolation (every 2nd x)
    for x in range(0, N, 2):
        if grid[x, 0] == 0:
            if bfs_percolate([(x, 0)], direction="vertical"):
                return

    # Try left-to-right percolation (every 2nd y)
    for y in range(0, N, 2):
        if grid[0, y] == 0:
            if bfs_percolate([(0, y)], direction="horizontal"):
                return


finding_cluster()

# Visualization
fig, ax = plt.subplots(1, 3, figsize=(14, 5))
ax[0].imshow(grid, cmap="gray_r")
ax[0].set_title("Grid (0=open, 1=blocked)")

ax[1].imshow(visited, cmap="viridis")
ax[1].set_title("Visited Sites")

ax[2].imshow(grid, cmap="gray_r")
ax[2].imshow(path2, cmap="autumn", alpha=0.7)
ax[2].set_title("Tetra-Shape Percolating Path (if found)")

plt.show()
