import heapq

initial_state = ((1, 2, 3, 4), (5, 6, 0, 8), (9, 10, 7, 11), (13, 14, 15, 12))

goal_state = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))


def is_zero(currState):
    for row, inner in enumerate(currState):
        for col, num in enumerate(inner):
            if num == 0:
                return row, col


def generate_states(curr_state):
    neighbors = []
    x, y = is_zero(curr_state)
    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    for dx, dy in moves:
        new_x = dx + x
        new_y = dy + y
        if 0 <= new_x < 4 and 0 <= new_y < 4:
            new_list = [list(inner) for inner in curr_state]
            new_list[x][y], new_list[new_x][new_y] = new_list[new_x][new_y], new_list[x][y]
            new_list = tuple(map(tuple, new_list))

            neighbors.append(new_list)

    return neighbors


def ucs(initialState):
    p_queue = [(0, initialState, [])]
    visited = set()
    while p_queue:
        current_cost, current_router, current_path = heapq.heappop(p_queue)

        if current_router == goal_state:
            return current_path + [current_router], current_cost

        if current_router in visited:
            continue  # skips the current iteration

        visited.add(current_router)
        for neighbor in generate_states(current_router):
            if neighbor not in visited:
                total_cost = current_cost + 1
                heapq.heappush(p_queue, (total_cost, neighbor, current_path + [current_router]))

    return None, float('inf')


bfs_path, cost = ucs(initial_state)
if bfs_path:
    print(cost)
    for state in bfs_path:
        print(state)
else:
    "No solution"
