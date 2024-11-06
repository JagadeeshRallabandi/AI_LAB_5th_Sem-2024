from collections import deque


def is_valid_state(state):
    M_left, C_left, M_right, C_right, _ = state
    # Check if the number of cannibals does not exceed missionaries on either side
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
                if (1 <= m + c <= 2) and (m <= M_left and c <= C_left):  # Move 1 or 2 people
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


def bfs():
    initial_state = (3, 3, 0, 0, 0)
    goal_state = (0, 0, 3, 3, 1)

    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        if current_state in visited:
            continue
        visited.add(current_state)

        if current_state == goal_state:
            return path + [current_state]

        for next_state in successors(current_state):
            queue.append((next_state, path + [current_state]))

    return None


result = bfs()
if result:
    print("Number of steps : ", len(result) - 1)
    print("Path to goal:")
    for step in result:
        print(step)
else:
    print("No solution found.")
