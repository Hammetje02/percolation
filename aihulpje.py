# kladblok met gpt

import numpy as np
import matplotlib.pyplot as plt

N = 100
np.random.seed(13)
p = 0.6  # adjust probability of open sites

# 0 = open, 1 = blocked
grid = np.where(np.random.random([N, N]) < p, 0, 1)

visited = np.zeros((N, N))
path2 = np.zeros((N, N))
found_path = False  # global flag to stop recursion once path found


def percolating(x, y, startx, starty, path):
    global visited, path2, found_path

    # Boundaries
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    if grid[x, y] == 1 or visited[x, y] == 1:
        return False

    # mark as visited
    visited[x, y] = 1
    path[x, y] = 1

    # Check percolation goal (horizontal or vertical)
    if (x == N - 1 and startx == 0) or (x == 0 and startx == N - 1):
        path2 += path
        found_path = True
        print("Horizontal percolation found!")
        return True
    if (y == N - 1 and starty == 0) or (y == 0 and starty == N - 1):
        path2 += path
        found_path = True
        print("Vertical percolation found!")
        return True

    # Explore neighbors if not already found
    if not found_path:
        if (percolating(x + 1, y, startx, starty, path.copy()) or
            percolating(x - 1, y, startx, starty, path.copy()) or
            percolating(x, y + 1, startx, starty, path.copy()) or
            percolating(x, y - 1, startx, starty, path.copy())):
            return True

    return False


def finding_cluster():
    global found_path, path2
    path = np.zeros((N, N))

    # Left to right
    for x in range(N):
        if found_path:
            break
        if grid[x, 0] == 0:
            if percolating(x, 0, x, 0, path.copy()):
                print("Found left-right percolation")
                break

    # Top to bottom (if not already found)
    if not found_path:
        for y in range(N):
            if grid[0, y] == 0:
                if percolating(0, y, 0, y, path.copy()):
                    print("Found top-bottom percolation")
                    break


finding_cluster()

# Plotting results
fig, ax = plt.subplots(1, 3, figsize=(14, 5))
ax[0].imshow(grid, cmap="gray_r")
ax[0].set_title("Grid (0=open, 1=blocked)")

ax[1].imshow(visited, cmap="viridis")
ax[1].set_title("Visited Sites")

ax[2].imshow(grid, cmap="gray_r")
ax[2].imshow(path2, cmap="autumn", alpha=0.7)
ax[2].set_title("Percolating Path (if found)")

plt.show()
