from collections import deque

initial_state = ((1, 2, 3),
                 (4, 0, 5),
                 (7, 8, 6))
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))


def display_puzzle(state):
    state1 = [list(inner) for inner in state]
    for row in state1:
        print(" ".join(str(tile) if tile != 0 else " " for tile in row))
    print()


def is_zero(state):
    for row, inner in enumerate(state):
        for col, num in enumerate(inner):
            if num == 0:
                return row, col


def gene_suc(state):
    neighbours = []
    x, y = is_zero(state)
    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    for dx, dy in moves:
        new_x = dx + x
        new_y = dy + y
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_list = [list(inner) for inner in state]
            new_list[x][y], new_list[new_x][new_y] = new_list[new_x][new_y], new_list[x][y]
            new_list = tuple(map(tuple, new_list))

            neighbours.append(new_list)
    return neighbours


def bfs(state):
    visited = set()
    queue = deque([(state, [])])
    visited.add(state)

    while queue:
        current_state, path = queue.popleft()
        if current_state == goal_state:
            return path + [current_state]
        for neighbor in gene_suc(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [current_state]))

    return None


def dfs(state):
    visited = set()
    stack = [(state, [])]
    visited.add(state)

    while stack:
        current_state, path = stack.pop()
        if current_state == goal_state:
            return path + [current_state]
        for neighbor in gene_suc(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [current_state]))

    return None


bfs_path = bfs(initial_state)
if bfs_path:
    for state in bfs_path:
        display_puzzle(state)
else:
    "No solution"

print("***********")

dfs_path = dfs(initial_state)
if dfs_path:
    for state in dfs_path:
        display_puzzle(state)
else:
    "No solution"
