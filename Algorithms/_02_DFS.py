def dfs_recursive(graph, node, visited):
    # Mark the node as visited
    visited.add(node)
    print(node,end=" ")  # Process the node (e.g., print it)

    # Recursively visit all the adjacent nodes
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node,end= " ")  # Process the node (e.g., print it)
            # Add all unvisited neighbors to the stack
            stack.extend(neighbor for neighbor in graph[node] if neighbor not in visited)


# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
visited = set()
dfs_recursive(graph, 'A', visited)
print("\n")
dfs_iterative(graph, 'A')
