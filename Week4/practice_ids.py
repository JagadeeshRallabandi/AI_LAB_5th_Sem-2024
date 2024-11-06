import heapq

def is_valid_state(state):
    M_left, C_left, M_right, C_right, _ = state
    if (M_left < 0 or C_left < 0 or M_right < 0 or C_right < 0 or
        (0 < M_left < C_left) or
        (0 < M_right < C_right)):
        return False
    return True

def successors(state):
    M_left, C_left, M_right, C_right, boat = state
    moves = []
    if boat == 0:  # Boat on left bank
        for m in range(3):
            for c in range(3):
                if (1 <= m + c <= 2) and (m <= M_left and c <= C_left):
                    new_state = (M_left - m, C_left - c, M_right + m, C_right + c, 1)
                    if is_valid_state(new_state):
                        moves.append(new_state)
    else:  # Boat on right bank
        for m in range(3):
            for c in range(3):
                if (1 <= m + c <= 2) and (m <= M_left and c <= C_left):
                    new_state = (M_left + m, C_left + c, M_right - m, C_right - c, 0)
                    if is_valid_state(new_state):
                        moves.append(new_state)
    return moves

def heuristic(state):
    M_left, C_left, M_right, C_right, _ = state
    return M_left + C_left  # Number of people left to move

def a_star():
    initial_state = (3, 3, 0, 0, 0)
    goal_state = (0, 0, 3, 3, 1)

    queue = []
    heapq.heappush(queue, (0 + heuristic(initial_state), 0, initial_state, []))
    visited = set()

    while queue:
        estimated_cost, cost, current_state, path = heapq.heappop(queue)

        if current_state in visited:
            continue
        visited.add(current_state)

        if current_state == goal_state:
            return path + [current_state]

        for next_state in successors(current_state):
            new_cost = cost + 1
            heapq.heappush(queue, (new_cost + heuristic(next_state), new_cost, next_state, path + [current_state]))

    return None

result = a_star()
if result:
    print(len(result)-1)
    print("Path to goal:")
    for step in result:
        print(step)
else:
    print("No solution found.")
