class GraphColoringCSP:
    def __init__(self, graph, colors):
        """
        graph: Dictionary where keys are nodes and values are lists of adjacent nodes
        colors: List of available colors
        """
        self.graph = graph
        self.colors = colors
        self.assignment = {}
        self.domains = {node: list(colors) for node in graph}

    def is_safe(self, node, color):
        """Check if assigning 'color' to 'node' is valid."""
        for neighbor in self.graph[node]:
            if neighbor in self.assignment and self.assignment[neighbor] == color:
                return False
        return True

    def degree_heuristic(self, unassigned_nodes):
        """
        Degree heuristic: Select the node with the most uncolored neighbors.
        """

        best_node = None
        max_uncolored_neighbors = -1

        for node in unassigned_nodes:
            uncolored_neighbors_count = 0
            for neighbor in self.graph[node]:
                if neighbor not in self.assignment:
                    uncolored_neighbors_count += 1
            if uncolored_neighbors_count > max_uncolored_neighbors:
                max_uncolored_neighbors = uncolored_neighbors_count
                best_node = node

        return best_node

    def mrv_heuristic(self, unassigned_nodes):
        best_node = None
        min_remaining_values = float('inf')

        for node in unassigned_nodes:
            remaining_values_count = len(self.domains[node])
            if remaining_values_count < min_remaining_values:
                min_remaining_values = remaining_values_count
                best_node = node

        return best_node

    def select_unassigned_variable(self):
        unassigned_nodes = [node for node in self.graph if node not in self.assignment]
        return self.mrv_heuristic(unassigned_nodes)

    def least_constraining_value(self, node):
        conflicts_list = []

        for color in self.domains[node]:
            conflicts = 0
            for neighbor in self.graph[node]:
                if color in self.domains[neighbor]:
                    conflicts += 1
            conflicts_list.append((color, conflicts))

        sorted_colors = sorted(conflicts_list, key=lambda x: x[1])
        return [color for color, _ in sorted_colors]

    def forward_checking(self, node, color):
        """Perform forward checking by removing the assigned color from neighbors' domains."""
        for neighbor in self.graph[node]:
            if neighbor not in self.assignment and color in self.domains[neighbor]:
                self.domains[neighbor].remove(color)
                # If domain of neighbor becomes empty, return failure
                if not self.domains[neighbor]:
                    return False
        return True

    def restore_domains(self, node, color, backup_domains):
        """Restore the domains after forward checking fails."""
        for neighbor in self.graph[node]:
            self.domains[neighbor] = backup_domains[neighbor][:]

    def maintaining_arc_consistency(self, node):
        """Maintains arc consistency using MAC."""
        # Implement basic arc consistency checks (e.g., AC-3)
        arcs = [(node, neighbor) for neighbor in self.graph[node] if neighbor not in self.assignment]
        while arcs:
            (xi, xj) = arcs.pop(0)
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False  # Domain wipeout, failure
                for xk in self.graph[xi]:
                    if xk != xj:
                        arcs.append((xk, xi))
        return True

    def revise(self, xi, xj):
        """Revise domains for arc consistency between xi and xj."""
        revised = False
        for color in self.domains[xi][:]:
            if all(color == val for val in self.domains[xj]):
                self.domains[xi].remove(color)
                revised = True
        return revised

    def backtrack(self):
        """Backtracking algorithm with forward checking and arc consistency."""
        if len(self.assignment) == len(self.graph):
            return True  # All nodes are assigned

        node = self.select_unassigned_variable()

        for color in self.least_constraining_value(node):
            if self.is_safe(node, color):
                self.assignment[node] = color  # Assign color

                # Backup current domain state for forward checking
                backup_domains = {n: self.domains[n][:] for n in self.graph[node]}

                if self.forward_checking(node, color) and self.maintaining_arc_consistency(node):
                    if self.backtrack():
                        return True

                # If failure, restore domains and unassign color
                self.restore_domains(node, color, backup_domains)
                del self.assignment[node]

        return False

    def solve(self):
        """Solve the graph coloring problem using backtracking and inference."""
        if self.backtrack():
            return self.assignment
        else:
            return None  # No solution found


# Example usage:
graph = {
    'V1': ['V2', 'V3','V5'],
    'V2': ['V1', 'V5', 'V6'],
    'V3': ['V1', 'V5', 'V6'],
    'V4': ['V6'],
    'V5': ['V1', 'V2','V3','V6'],
    'V6': ['V4', 'V3','V5','V2']
}

colors = ['Red', 'Green', 'Blue']

solver = GraphColoringCSP(graph, colors)
solution = solver.solve()

if solution:
    print("Solution found:", solution)
else:
    print("No solution found.")
