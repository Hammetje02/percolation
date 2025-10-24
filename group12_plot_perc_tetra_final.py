import numpy as np
import matplotlib.pyplot as plt

N = 500
np.random.seed(13)


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


def bfs(x, y, visited, grid,mode=0):
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


def finding_path(grid, visited, mode=0):
    N = grid.shape[0]
    if mode==0:
        for x in range(N):
            if bfs(x, 0, visited, grid, mode):
                return True

        for y in range(N):
            if bfs(0, y, visited, grid, mode):
                return True
    else:
        for x in range(0,N,2):
            if bfs(x, 0, visited, grid, mode):
                return True

        for y in range(0,N,2):
            if bfs(0, y, visited, grid, mode):
                return True
    return False


def simulate_model(max_trials=20):
    max_trials=20
    p_values = np.arange(0.40, 0.66, 0.01)
    results = np.zeros((2,int(p_values.shape[0]))) #[0] = normal, [1] is tetra
    mode_list = ["normal", "tetra"]

    for i in range(2):
        for pj in range(len(p_values)):
            p = p_values[pj]
            success_count = 0
            for _ in range(max_trials):
                visited = np.zeros([N,N])
                grid = np.where(np.random.random((N, N)) < p, 0, 1)
                if finding_path(grid, visited, i):
                    success_count += 1

            results[i,pj] = success_count / max_trials
            print(f"{mode_list[i]} | p={p:.2f} -> {success_count}/{max_trials} percolations")

    return results, p_values


results, p_vals = simulate_model(max_trials=20)
results_standard = results[0]
results_tetra = results[1]


plt.figure(figsize=(10, 6))
plt.plot(p_vals, results_standard, "-o", label="Standard model")
plt.plot(p_vals, results_tetra, "-s", label="Tetra model")
plt.xlabel("Open site probability p")
plt.ylabel("Percolation frequency (fraction of 20 trials)")
plt.title("Percolation Transition (0.45 ≤ p ≤ 0.65, 20 trials per p)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.show()
