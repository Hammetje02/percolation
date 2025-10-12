import numpy as np
import matplotlib.pyplot as plt

N = 150
np.random.seed(13)
visited = np.zeros([N,N])
# percolating_cluster = np.zeros([N,N])
# path2 = np.zeros([N,N])
# p = float(input("Insert porosity"))
p = 0.59
grid = np.where(np.random.random([N,N]) < p, 0, 1)  # 0 is open path
# grid = grid + driehoek

def neighbours(coords, visited):
    global grid
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


def bfs(x, y, visited):
    """Does breadth first seacrh starting from given coordinates.

    Args:
        x (int): _description_
        y (int): _description_
        visited (_type_): _description_

    Returns:
        boolean: _description_
    """
    if grid[x,y] == 1 or visited[x,y] == 1:
        return False

    queue = [[x,y]]
    visited[x,y] = 1
    while queue:
        coords = queue.pop()

        if perc_condition(coords, x, y):
            return True
        nn_list, visited = neighbours(coords, visited)

        for nn in nn_list:
            queue.insert(0, nn)
    return False


def bfs_path(x, y, path):
    """Does breadth first seacrh starting from given coordinates.

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
        nn_list, path = neighbours(coords, path)

        for nn in nn_list:
            queue.insert(0, nn)
    return path


def finding_path(visited):
    for x in range(N):
        if bfs(x, 0, visited):
            # run cluster creator
            path = np.zeros_like(visited)
            path = bfs_path(x,0, path)
            return path, visited

    for y in range(N):
        # visited = np.zeros((N,N))
        if bfs(0, y, visited):
            # run cluster creator
            path = np.zeros_like(visited)
            path = bfs_path(0,y, path)
            return path, visited

    return np.array([1]), visited # returns a 1d array with 1 element if nothing found


path, visited = finding_path(visited)
# print(path.shape[0])
if path.shape[0] != 1:
    plt.title("percolating cluster")
    plt.imshow(path)
    plt.colorbar()
    plt.show()
    plt.title("grid")
    plt.imshow(visited)
    plt.colorbar()
    plt.show()
else:
    plt.title("all visited sites")
    plt.imshow(visited)
    plt.colorbar()
    plt.show()

# def percolating(x, y, startx, starty, path):
#     global visited
#     global path2
#     if x >= N or y >= N or x <= -1 or y <= 1:
#         return False
#     if grid[x, y] == 1 or visited[x,y] >= 1:
#         # terminates this recursion
#         visited = np.add(visited, path)
#         path = np.zeros((N,N))
#         print("a")
#         return False
#     # the path can be taken so take the step
#     visited[x,y] = 1
#     # horizontal cluster
#     if (x == (N-1) and startx == 0) or (x == 0 and startx == (N-1)) :
#         # return coordinates to make in another function the coordinates which belong to percolating cluster
#         #return cluster, ensure that you do not make to many clusters
#         path[x,y] = 1
#         path2[x,y] = 1
#         print("b")
#         return True
#     #verical cluster
#     if (y == (N-1) and starty == 0) or (y == 0 and starty == (N-1)) :
#         # return coordinates to make in another function the coordinates which belong to percolating cluster
#         path[x,y] = 1
#         path2 = path[x,y]
#         print("c")
#         return True

#     # propose new positions:
#     path[x,y] = 1
#     # visited[x,y] = 1
#     return percolating(x +1 , y, startx, starty, path) or percolating(x - 1, y, startx, starty, path) or percolating(x , y + 1, startx, starty, path) or percolating(x , y - 1, startx, starty, path)


# # Clelia's idea: making it flow, through the grid, basicly in the style of breadth first search.+
# def finding_cluster():
#     path = np.zeros([N,N])
#     for x in range(N):
#         print(percolating(x,0, x,0, path))
#         if percolating(x,0, x,0, path):
#             print("found")
#             plt.imshow(path2)
#             break
#     for y in range(N):
#         if percolating(0,y, 0, y, path):
#             print("found")
#             plt.imshow(path2)
#             break
# finding_cluster()
# plt.imshow(path2)
# plt.colorbar()
# plt.show()