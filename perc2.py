import numpy as np
import matplotlib.pyplot as plt

N = 100
np.random.seed(13)
visited = np.zeros([N,N])
path2 = np.zeros([N,N])
percolating_cluster = np.zeros([N,N])
p = 0.9
grid = np.where(np.random.random([N,N]) < p, 0, 1)  # 0 is open path

def percolating(x, y, startx, starty, path):
    global visited
    if grid[x, y] == 1 or visited[x,y] == 1:
        # terminates this recursion
        visited = np.add(visited, path)
        path = np.zeros((N,N))
        print("a")
        return False
    # the path can be taken so take the step
    visited[x,y] = 1
    # horizontal cluster
    if (x == (N-1) and startx == 0) or (x == 0 and startx == (N-1)) :
        # return coordinates to make in another function the coordinates which belong to percolating cluster
        #return cluster, ensure that you do not make to many clusters
        path[x,y] = 1
        path2[x,y] = 1
        print("b")
        return True
    #verical cluster
    if (y == (N-1) and starty == 0) or (y == 0 and starty == (N-1)) :
        # return coordinates to make in another function the coordinates which belong to percolating cluster
        path[x,y] = 1
        path2 = path[x,y]
        print("c")
        return True

    # propose new positions:
    path[x,y] = 1
    # visited[x,y] = 1
    return percolating(x +1 , y, startx, starty, path) or percolating(x - 1, y, startx, starty, path) or percolating(x , y+1, startx, starty, path) or percolating(x , y-1, startx, starty, path)


# Clelia's idea: making it flow, through the grid, basicly in the style of breadth first search.+
def finding_cluster():
    path = np.zeros([N,N])
    for x in range(N):
        print(percolating(x,0, x,0, path))
        if percolating(x,0, x,0, path):
            print("found")
            plt.imshow(path2)
            break
    for y in range(N):
        if percolating(0,y, 0, y, path):
            print("found")
            plt.imshow(path2)
            break
finding_cluster()
plt.imshow(visited)
plt.colorbar()
plt.show()

# print(not 0)

# in mathematica it can be done with graph theory.
# z = np.zeros_like([1])
# def test():
#     z[0] = 2
# test()
# print(z)