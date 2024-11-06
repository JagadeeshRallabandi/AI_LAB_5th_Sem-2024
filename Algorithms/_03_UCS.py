import heapq


def uniform_cost_search(graph, start, goal):
    # Priority queue to store (cost, node, path)
    priority_queue = [(0, start, [])]
    visited = set()

    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)

        # Avoid revisiting nodes
        if node in visited:
            continue  # skips the iteration
        visited.add(node)

        # Update the path
        path = path + [node]

        # Goal check
        if node == goal:
            return path, cost

        # Expand neighbors
        for neighbor, edge_cost in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + edge_cost, neighbor, path))

    return None, float('inf')  # In case there is no path


# Example graph representation
graph = {
    'A': [('B', 90), ('C', 80)],
    'B': [('A', 90), ('E', 211)],
    'C': [('D', 97), ('A', 80)],
    'D': [('C', 97), ('E', 101)],
    'E': [('B', 211), ('D', 101)]
}

# Running UCS
start_node = 'A'
goal_node = 'D'
path, total_cost = uniform_cost_search(graph, start_node, goal_node)

print(f"Path: {path}")
print(f"Total cost: {total_cost}")
