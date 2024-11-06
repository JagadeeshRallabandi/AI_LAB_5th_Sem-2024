import heapq


class Graph:
    def __init__(self):
        self.edges = {}
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Add edge from `from_node` to `to_node` with the given weight
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight

    def heuristic(self, node, goal):
        # Define a simple heuristic function. This can be changed based on the problem.
        return abs(node - goal)


def best_first_search(graph, start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (graph.heuristic(start, goal), start))

    came_from = {}
    came_from[start] = None

    while priority_queue:
        # Get the node with the lowest heuristic value
        _, current_node = heapq.heappop(priority_queue)

        if current_node == goal:
            # Reconstruct path from start to goal
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            return path

        # Explore neighbors
        for neighbor in graph.edges.get(current_node, []):
            if neighbor not in came_from:
                priority = graph.heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (priority, neighbor))
                came_from[neighbor] = current_node

    return None  # Return None if no path is found


# Example usage:
g = Graph()
g.add_edge(1, 2, 1)
g.add_edge(1, 3, 1)
g.add_edge(2, 4, 1)
g.add_edge(3, 4, 1)
g.add_edge(4, 5, 1)
g.add_edge(3, 6, 1)

start = 1
goal = 5
path = best_first_search(g, start, goal)
print(f"Path found: {path}")
