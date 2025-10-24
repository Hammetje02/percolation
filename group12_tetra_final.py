import numpy as np
import matplotlib.pyplot as plt

N = 100  # small N to showcase the path better in plot
np.random.seed(13)
visited = np.zeros([N,N])
# p = float(input("Insert porosity"))
p = 0.48
grid = np.where(np.random.random([N,N]) < p, 0, 1)  # 0 is open path

def neighbours(coords, visited, grid):
    x,y = coords
    nn_list = []

    if (x+1) < N and not visited[x + 1, y] and grid[x + 1, y] == 0:
        visited[x + 1, y] = 1
        nn_list.append([x + 1, y])
    if (x-1) >= 0 and not visited[x - 1, y] and grid[x - 1, y] == 0:
        visited[x - 1, y] = 1
        nn_list.append([x - 1, y])
    if (y+1) < N and not visited[x, y + 1] and grid[x, y + 1] == 0:
        visited[x, y + 1] = 1
        nn_list.append([x, y + 1])
    if (y-1) >= 0 and not visited[x, y - 1] and grid[x, y - 1] == 0:
        visited[x, y - 1] = 1
        nn_list.append([x, y - 1])

    return nn_list, visited


def neighbours_tetra(coords, visited, grid):
    x,y = coords
    nn_list = []

    if (x+1) < N and (y+1) < N and not visited[x + 1, y+1] and grid[x + 1, y+1] == 0:
        visited[x + 1, y+1] = 1
        nn_list.append([x + 1, y+1])
    if (x-1) >= 0 and (y-1) >= 0 and not visited[x - 1, y-1] and grid[x - 1, y-1] == 0:
        visited[x - 1, y-1] = 1
        nn_list.append([x - 1, y-1])
    if (y+1) < N and (x-1) >= 0 and not visited[x-1, y + 1] and grid[x-1, y + 1] == 0:
        visited[x-1, y + 1] = 1
        nn_list.append([x-1, y + 1])
    if (y-1) >= 0 and (x+1) < N and  not visited[x+1, y - 1] and grid[x+1, y - 1] == 0:
        visited[x+1, y - 1] = 1
        nn_list.append([x+1, y - 1])
    if (x+2) < N and not visited[x + 2, y] and grid[x + 2, y] == 0:
        visited[x + 2, y] = 1
        nn_list.append([x + 2, y])
    if (x-2) >= 0 and not visited[x - 2, y] and grid[x - 2, y] == 0:
        visited[x - 2, y] = 1
        nn_list.append([x - 2, y])

    return nn_list, visited


def perc_condition(coords, startx, starty):
    x,y = coords

    if startx == 0 and x == N-1:
        return True
    if starty == 0 and y== N-1:
        return True
    # if x == 0 and startx == N-1:
    #     return True
    # if y == 0 and starty == N-1:
    #     return True

    return False


def bfs(x, y, visited, grid,mode=1):
    """Does breadth first seacrh starting from given coordinates.

    Args:
        x (int): _description_
        y (int): _description_
        visited (_type_): _description_
        mode: 0 if normal, 1 if tetra

    Returns:
        boolean: _description_
    """
    if grid[x,y] == 1 or visited[x,y] == 1:
        return False

    queue = [[x,y]]
    visited[x,y] = 1
    if mode == 0:
        while queue:
            coords = queue.pop()

            if perc_condition(coords, x, y):
                return True
            nn_list, visited = neighbours(coords, visited, grid)

            for nn in nn_list:
                queue.insert(0, nn)
    elif mode == 1:
        while queue:
            coords = queue.pop()

            if perc_condition(coords, x, y):
                return True
            nn_list, visited = neighbours_tetra(coords, visited, grid)

            for nn in nn_list:
                queue.insert(0, nn)
    return False


def finding_path(grid, visited, mode=1):
    N = grid.shape[0]
    for x in range(0,N,2):
        if bfs(x, 0, visited, grid, mode):
            path = np.zeros_like(visited)
            path = bfs_path(x,0, path, grid, mode)
            return path, visited

    for y in range(0,N,2):
        if bfs(0, y, visited, grid, mode):
            path = np.zeros_like(visited)
            path = bfs_path(0,y, path, grid, mode)
            return path, visited
    return np.array([1]), visited

def bfs_path(x, y, path, grid, mode):
    """Does breadth first search starting from given coordinates.

    Args:
        x (int): _description_
        y (int): _description_
        visited (_type_): _description_

    Returns:
        boolean: _description_
    """

    queue = [[x,y]]
    path[x,y] = 1
    while queue:
        coords = queue.pop()
        nn_list, path = neighbours_tetra(coords, path, grid)

        for nn in nn_list:
            queue.insert(0, nn)
    return path

path, visited = finding_path(grid, visited, 1)

if path.shape[0] != 1:
    fig, ax = plt.subplots(1, 3, figsize=(14, 5))
    ax[0].imshow(grid, cmap="gray_r")
    ax[0].set_title("Grid")

    ax[1].imshow(visited, cmap="viridis")
    ax[1].set_title("Visited Sites")

    ax[2].imshow(grid, cmap="gray_r")
    ax[2].imshow(path, cmap="winter", alpha=0.6)
    ax[2].set_title("Percolating Path")

    plt.show()
else:
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    ax[0].imshow(grid, cmap="gray_r")
    ax[0].set_title("Grid")

    ax[1].imshow(visited, cmap="viridis")
    ax[1].set_title("Visited Sites")
    plt.show()