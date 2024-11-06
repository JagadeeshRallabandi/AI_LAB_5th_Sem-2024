from collections import deque


def bfs(graph, start):
    # Initialize a queue and add the starting node
    queue = deque([start])
    # Keep track of visited nodes to avoid cycles
    visited = set([start])

    while queue:
        # Pop the first node in the queue
        node = queue.popleft()
        print(node, end=' ')

        # Add all unvisited neighbors to the queue
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)


# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

bfs(graph, 'A')
