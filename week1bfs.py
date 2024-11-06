from collections import deque

# Define the Node class
class Node:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth

    # Method to retrieve the solution path from the initial state to this node
    def get_path(self):
        path = []
        node = self
        while node.parent is not None:
            path.append(node.action)
            node = node.parent
        return path[::-1]  # Reverse the path to get the order from start to goal

# Goal state for the 8-puzzle
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Check if the current state is the goal
def goal_test(state):
    return state == goal_state

# Generate successors of a given state
def get_successors(state):
    row, col = next((r, c) for r in range(3) for c in range(3) if state[r][c] == 0)
    successors = []
    directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
    
    for action, (dr, dc) in directions.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [row[:] for row in state]
            new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
            successors.append((action, new_state))
    
    return successors

# Breadth-First Search (BFS) function
def bfs(initial_state):
    frontier = deque([Node(initial_state)])
    explored = set()

    while frontier:
        node = frontier.popleft()  # Remove from the front of the queue
        if goal_test(node.state):
            return node.get_path()  # Solution found
        explored.add(tuple(map(tuple, node.state)))  # Mark state as explored
        
        for action, successor in get_successors(node.state):
            if tuple(map(tuple, successor)) not in explored:
                child_node = Node(successor, node, action, node.depth + 1)
                frontier.append(child_node)

    return None  # No solution found

# Example usage of BFS
initial_state = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
print("BFS Solution:", bfs(initial_state))
