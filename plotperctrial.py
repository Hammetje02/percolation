import numpy as np
import matplotlib.pyplot as plt
from collections import deque

N = 200  # grid size (increase carefully if you want more precision)
np.random.seed(13)

# ==========================================================
# --- BFS percolation function (non-recursive) ---
# ==========================================================
def bfs_percolate(grid, neighbor_offsets, direction="vertical"):
    N = grid.shape[0]
    visited = np.zeros_like(grid)
    queue = deque()

    # Start from top or left edge
    if direction == "vertical":
        start_positions = [(0, y) for y in range(N)]
    else:
        start_positions = [(x, 0) for x in range(N)]

    for pos in start_positions:
        x, y = pos
        if grid[x, y] == 0:
            queue.append((x, y))
            visited[x, y] = 1

    while queue:
        x, y = queue.popleft()

        # Check if we reached the opposite side
        if (direction == "vertical" and x == N - 1) or (direction == "horizontal" and y == N - 1):
            return True

        for dx, dy in neighbor_offsets:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                if grid[nx, ny] == 0 and visited[nx, ny] == 0:
                    visited[nx, ny] = 1
                    queue.append((nx, ny))

    return False


# ==========================================================
# --- Simulation function ---
# ==========================================================
def simulate_model(model_type="standard", max_trials=20):
    if model_type == "standard":
        neighbor_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    elif model_type == "tetra":
        neighbor_offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1), (2, 0), (-2, 0)]
    else:
        raise ValueError("Unknown model type.")

    # Focused p range for transition zone
    p_values = np.arange(0.45, 0.65 + 1e-6, 0.01)
    results = []

    for p in p_values:
        success_count = 0
        for _ in range(max_trials):
            grid = np.where(np.random.random((N, N)) < p, 0, 1)
            if bfs_percolate(grid, neighbor_offsets, direction="vertical"):
                success_count += 1

        results.append((p, success_count))
        print(f"{model_type.upper()} | p={p:.2f} → {success_count}/{max_trials} percolations")

    return results


# ==========================================================
# --- Run simulations for both models ---
# ==========================================================
results_standard = simulate_model("standard", max_trials=20)
results_tetra = simulate_model("tetra", max_trials=20)

# Convert to arrays
p_vals_standard, counts_standard = zip(*results_standard)
p_vals_tetra, counts_tetra = zip(*results_tetra)

# Normalize (fraction of percolations)
perc_rate_standard = np.array(counts_standard) / 20.0
perc_rate_tetra = np.array(counts_tetra) / 20.0

# ==========================================================
# --- Plot fine transition region ---
# ==========================================================
plt.figure(figsize=(10, 6))
plt.plot(p_vals_standard, perc_rate_standard, "-o", label="Standard model (4-neighbor)")
plt.plot(p_vals_tetra, perc_rate_tetra, "-s", label="Tetra model")
plt.xlabel("Open site probability p")
plt.ylabel("Percolation frequency (fraction of 20 trials)")
plt.title("Percolation Transition (0.45 ≤ p ≤ 0.65, 20 trials per p)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.show()
