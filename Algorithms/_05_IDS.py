def depth_limited_search(graph, start, goal, depth_limit):
    def dls(node, goal, depth):
        # If depth limit is reached, return failure
        if node == goal:
            return [node]

        if depth == 0:
            return None

        # If the node is the goal, return the path

        # Explore neighbors
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path = dls(neighbor, goal, depth - 1)
                if path is not None:
                    return [node] + path

        # If no path is found, return failure
        return None

    # Initialize visited set and start the search
    visited = set()
    visited.add(start)
    return dls(start, goal, depth_limit)


# Example graph representation
def dfs_limited(graph, start, goal, depth_limit):
    stack = [(start, 0)]  # Stack of tuples (node, current_depth)
    visited = set()

    while stack:
        node, depth = stack.pop()

        if node == goal:
            return True

        if depth < depth_limit:
            if node not in visited:
                visited.add(node)
                for neighbor in reversed(graph[node]):  # Reverse to maintain order of exploration
                    stack.append((neighbor, depth + 1))

    return False


def iterative_deepening_search(graph, start, goal, max_depth):
    for depth in range(max_depth + 1):
        if dfs_limited(graph, start, goal, depth):
            print("min-depth :", depth)
            return True
    return False


# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

start_node = 'A'
goal_node = 'F'
max_depth = 2

found = iterative_deepening_search(graph, start_node, goal_node, max_depth)
print(f"Goal {goal_node} found: {found}")
