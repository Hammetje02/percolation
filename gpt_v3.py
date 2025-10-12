import numpy as np
import matplotlib.pyplot as plt

N = 100
np.random.seed(13)
p = 0.6
grid = np.where(np.random.random([N, N]) < p, 0, 1)  # 0 is open

def neighbours(coords, visited):
    x, y = coords
    nn_list = []
    # four neighbors; mark visited when enqueueing to avoid duplicates
    if x + 1 < N and not visited[x + 1, y] and grid[x + 1, y] == 0:
        visited[x + 1, y] = 1
        nn_list.append([x + 1, y])
    if x - 1 >= 0 and not visited[x - 1, y] and grid[x - 1, y] == 0:
        visited[x - 1, y] = 1
        nn_list.append([x - 1, y])
    if y + 1 < N and not visited[x, y + 1] and grid[x, y + 1] == 0:
        visited[x, y + 1] = 1
        nn_list.append([x, y + 1])
    if y - 1 >= 0 and not visited[x, y - 1] and grid[x, y - 1] == 0:
        visited[x, y - 1] = 1
        nn_list.append([x, y - 1])
    return nn_list, visited

def perc_condition(coords, startx, starty):
    # Determine whether this BFS was started from a vertical or horizontal boundary
    # and only check the appropriate opposite boundary.
    x, y = coords
    # vertical start: top (startx==0) or bottom (startx==N-1)
    if startx == 0 and x == N - 1:   # top -> bottom
        return True
    if startx == N - 1 and x == 0:   # bottom -> top
        return True
    # horizontal start: left (starty==0) or right (starty==N-1)
    if starty == 0 and y == N - 1:   # left -> right
        return True
    if starty == N - 1 and y == 0:   # right -> left
        return True
    return False

def bfs(start_x, start_y, visited):
    """Return True if cluster starting at (start_x,start_y) percolates."""
    if grid[start_x, start_y] != 0:
        return False
    queue = [[start_x, start_y]]
    visited[start_x, start_y] = 1
    while queue:
        coords = queue.pop()     # pop from end; we insert new at front -> FIFO behavior
        if perc_condition(coords, start_x, start_y):
            return True
        nn_list, visited = neighbours(coords, visited)
        for nn in nn_list:
            queue.insert(0, nn)
    return False

def bfs_path(start_x, start_y):
    """Return array with 1s for the explored cluster starting at (start_x,start_y)."""
    path = np.zeros((N, N), dtype=int)
    if grid[start_x, start_y] != 0:
        return path
    queue = [[start_x, start_y]]
    path[start_x, start_y] = 1
    while queue:
        coords = queue.pop()
        nn_list, path = neighbours(coords, path)
        for nn in nn_list:
            queue.insert(0, nn)
    return path

def finding_path():
    # 1) Check vertical percolation (top -> bottom), start from all open cells on top row
    for y in range(N):
        if grid[0, y] == 0:
            visited = np.zeros((N, N), dtype=int)
            if bfs(0, y, visited):
                return bfs_path(0, y)

    # 2) Check vertical percolation starting from bottom (optional)
    for y in range(N):
        if grid[N-1, y] == 0:
            visited = np.zeros((N, N), dtype=int)
            if bfs(N-1, y, visited):
                return bfs_path(N-1, y)

    # 3) Check horizontal percolation (left -> right), start from all open cells on left column
    for x in range(N):
        if grid[x, 0] == 0:
            visited = np.zeros((N, N), dtype=int)
            if bfs(x, 0, visited):
                return bfs_path(x, 0)

    # 4) Check horizontal starting from right (optional)
    for x in range(N):
        if grid[x, N-1] == 0:
            visited = np.zeros((N, N), dtype=int)
            if bfs(x, N-1, visited):
                return bfs_path(x, N-1)

    return None

path = finding_path()
if path is not None:
    plt.imshow(path, origin='upper')
    plt.title("Percolating cluster (1 = cluster)")
    plt.colorbar()
    plt.show()
else:
    print("No percolating cluster found (in the searched directions).")
    # Optional: show the grid (0=open, 1=blocked)
    plt.imshow(grid, origin='upper')
    plt.title("Grid (0=open, 1=blocked)")
    plt.colorbar()
    plt.show()
