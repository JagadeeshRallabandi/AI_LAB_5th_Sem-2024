import random
import time
import heapq
import sys
import psutil
from copy import deepcopy


class PuzzleSolver:
    def __init__(self):
        self.goal_state = self.generate_random_goal_state()
        self.initial_state = self.generate_solvable_initial_state()

    def generate_random_goal_state(self):
        while True:
            state = random.sample(range(9), 9)
            state = [state[:3], state[3:6], state[6:]]
            if self.is_solvable(state):
                return state

    def generate_solvable_initial_state(self):
        while True:
            state = random.sample(range(9), 9)
            state = [state[:3], state[3:6], state[6:]]
            if self.is_solvable(state):
                return state

    def is_solvable(self, state):
        flat_state = []

        for row in state:
            for num in row:
                if num != 0:
                    flat_state.append(num)

        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        return inversions % 2 == 0

    def misplaced_tiles(self, state):
        count = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != self.goal_state[i][j] and state[i][j] != 0:
                    count += 1
        return count

    def manhattan_distance(self, state):
        goal_positions = {}
        for i in range(3):
            for j in range(3):
                goal_positions[self.goal_state[i][j]] = (i, j)

        distance = 0
        for i in range(3):
            for j in range(3):
                tile = state[i][j]
                if tile != 0:
                    goal_x, goal_y = goal_positions[tile]
                    distance += abs(goal_x - i) + abs(goal_y - j)
        return distance

    def heuristic_consistency_check(self, state):
        return self.manhattan_distance(state) >= self.misplaced_tiles(state)

    def a_star_search(self, heuristic):
        initial_key = tuple(tuple(row) for row in self.initial_state)
        goal_key = tuple(tuple(row) for row in self.goal_state)

        start_time = time.time()

        queue = [(0 + heuristic(self.initial_state), 0, self.initial_state, [])]
        visited = {initial_key: 0}

        while queue:
            estimated_cost, cost, current, path = heapq.heappop(queue)
            current_key = tuple(tuple(row) for row in current)

            if current_key == goal_key:
                end_time = time.time()
                return {
                    "path": path + [current],
                    "steps": len(path),
                    "cpu_time": end_time - start_time,
                    "memory": psutil.Process().memory_info().rss / 1024
                }

            x, y = None, None
            for row, inner in enumerate(current):
                for col, num in enumerate(inner):
                    if num == 0:
                        x = row
                        y = col

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 3 and 0 <= new_y < 3:
                    new_state = [list(inner) for inner in current_key]
                    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                    new_cost = cost + 1
                    new_key = tuple(tuple(row) for row in new_state)

                    if new_key not in visited or visited[new_key] > new_cost:
                        visited[new_key] = new_cost
                        heapq.heappush(queue, (new_cost + heuristic(new_state), new_cost, new_state, path + [current]))

        return None

    def solve_with_misplaced_tiles(self):
        return self.a_star_search(self.misplaced_tiles)

    def solve_with_manhattan_distance(self):
        return self.a_star_search(self.manhattan_distance)

    def tabulate_results(self):
        print("Initial State:")
        for row in self.initial_state:
            print(row)
        print("\nGoal State:")
        for row in self.goal_state:
            print(row)

        print("\nUsing Misplaced Tiles Heuristic:")
        result_mt = self.solve_with_misplaced_tiles()
        self.display_result(result_mt)

        print("\nUsing Manhattan Distance Heuristic:")
        result_md = self.solve_with_manhattan_distance()
        self.display_result(result_md)

    def display_result(self, result):
        if result:
            print(f"Number of steps: {result['steps']}")
            print(f"CPU time taken: {result['cpu_time']} seconds")
            print(f"Memory consumed: {result['memory']} KB")
            print("Path to goal:")
            for step in result["path"]:
                for row in step:
                    print(row)
                print()
        else:
            print("No solution found.")


# Run the PuzzleSolver and tabulate results
solver = PuzzleSolver()
solver.tabulate_results()
