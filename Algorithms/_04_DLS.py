def depth_limited_search(graph, start, goal, depth_limit):
    def recursive_dls(node, goal, depth):
        # If the depth limit is reached, and it's not the goal, return None
        if depth == 0:
            return [node] if node == goal else None

        # If the goal is found and the depth is not zero, return the path
        if node == goal:
            return [node]

        # Explore neighbors
        for neighbor in graph.get(node, []):
            result = recursive_dls(neighbor, goal, depth - 1)
            if result is not None:
                return [node] + result

        return None  # If no path is found within the depth limit

    return recursive_dls(start, goal, depth_limit)


graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

# Running DLS
start_node = 'A'
goal_node = 'F'
depth_limit = 3
path = depth_limited_search(graph, start_node, goal_node, depth_limit)

print(f"Path: {path}")
