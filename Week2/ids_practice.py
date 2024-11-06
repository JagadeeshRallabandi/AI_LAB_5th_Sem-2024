
moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]

maze = (
    ('S', 0, 0, 1, 0, 0),
    (1, 1, 0, 1, 1, 0),
    (0, 0, 0, 0, 1, 0),
    (1, 1, 1, 0, 1, 0),
    (0, 0, 0, 0, 0, 'G')
)

def positions(_maze):
    start = goal = None
    for row, inner in enumerate(_maze):
        for col, num in enumerate(inner):
            if num == 'S':
                start = (row, col)
            elif num == 'G':
                goal = (row, col)
    return start, goal

def is_valid_move(_maze, x, y):
    return 0 <= x < len(_maze) and 0 <= y < len(_maze[0]) and _maze[x][y] != 1

def depth_limited_search(_maze, _current, _goal, depth_limit, _path):
    x, y = _current
    if _current == _goal:
        return _path
    if depth_limit <= 0:
        return None

    for move in moves:
        dx, dy = move
        new_x, new_y = x + dx, y + dy
        new_position = (new_x, new_y)

        if is_valid_move(_maze, new_x, new_y) and new_position not in _path:
            result = depth_limited_search(_maze, new_position, _goal, depth_limit - 1, _path + [new_position])
            if result:
                return result
    return None

def iterative_deepening_search(_maze):
    _start, _goal = positions(_maze)

    if not _start or not _goal:
        return None

    depth = 0
    while True:
        result = depth_limited_search(_maze, _start, _goal, depth, [_start])
        if result:
            return result
        depth += 1

solution_path = iterative_deepening_search(maze)

if solution_path:
    print("Solution path found with {} steps.".format(len(solution_path) - 1))
    for step, position in enumerate(solution_path):
        print("Step {}: Position {}".format(step, position))
else:
    print("No solution found.")
