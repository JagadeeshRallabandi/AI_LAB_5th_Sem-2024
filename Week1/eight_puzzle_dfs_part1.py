def dfs(start, end):
    def possibile_states(state):
        possibilities = []
        blank_position = state.index(0)
        row, col = divmod(blank_position, 3)
        moves = {
            'left': (row, col - 1),
            'right': (row, col + 1),
            'up': (row - 1, col),
            'down': (row + 1, col)
        }
        for move, (r, c) in moves.items():
            if 0 <= r < 3 and 0 <= c < 3:
                new_blank_position = r * 3 + c
                new_state = list(state)
                new_state[blank_position], new_state[new_blank_position] = (
                    new_state[new_blank_position],
                    new_state[blank_position],
                )
                possibilities.append((tuple(new_state), move))
        return possibilities

    def reconstruct_path(parent_dict, current):
        path = [(current, None)]
        while current in parent_dict:
            current, move = parent_dict[current]
            path.append((current, move))
        path.reverse()
        return path

    start = tuple(start)
    end = tuple(end)
    if start == end:
        return [(start, None)]

    stack = [(start, None)]
    parent_dict = {}
    visited = set()
    parent_dict[start] = (None, None)
    visited.add(start)

    while stack:
        current, _ = stack.pop()
        for neighbor, move in possibile_states(current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, move))
                parent_dict[neighbor] = (current, move)
                if neighbor == end:
                    return reconstruct_path(parent_dict, neighbor)

    return None

def parse_input(user_input):
    return [int(x) for x in user_input.split()]

if __name__ == "__main__":
    print("Enter start state:")
    start_input = input()
    print("Enter end state:")
    end_input = input()
    start = parse_input(start_input)
    end = parse_input(end_input)
    path = dfs(start, end)
    if path:
        print("Solution found:")
        for state, move in path:
            print(state)
            if move:
                print(f"Move: {move}")
        print(f"The number of moves is {len(path) - 2}")
    else:
        print("No solution found.")