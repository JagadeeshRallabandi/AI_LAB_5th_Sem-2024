import heapq
import itertools
import random
import time
import psutil


class Puzzle:
    def __init__(self, start=None, goal=None):
        self.start = start if start else self.random_state()
        self.goal = goal if goal else self.random_state()

        while not self.isSolvable(self.start):
            self.start = self.random_state()
        while not self.isSolvable(self.goal):
            self.goal = self.random_state()

    def random_state(self):
        state = list(range(9))
        random.shuffle(state)
        return tuple(state)

    def isSolvable(self, state):
        inversion_count = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                    inversion_count += 1

        return inversion_count % 2 == 0

    def heuristic_misplaced_tiles(self, state):
        misplaced_tile_count = 0
        for i in range(9):
            if state[i] != self.goal[i] and state[i] != 0:
                misplaced_tile_count += 1

        return misplaced_tile_count

    def heuristic_manhattan_distance(self, state):
        distance = 0
        for i in range(9):
            if state[i] != 0:
                x1, y1 = divmod(i, 3)
                x2, y2 = divmod(self.goal.index(state[i]), 3)
                distance += abs(x1 - x2) + abs(y1 - y2)
        return distance

    def generate_all_possible_states(self):
        for perm in itertools.permutations(range(9)):
            if self.isSolvable(perm):
                yield perm

    def a_star_search(self, heuristic):
        frontier = []
        heapq.heappush(frontier, (0, self.start, []))
        explored = {}
        explored[self.start] = 0
        while frontier:
            current_cost, current, path = heapq.heappop(frontier)

            if current == self.goal:
                return path

            for move, next_state in self.get_successors(current):
                new_cost = current_cost + 1
                if next_state not in explored or new_cost < explored[next_state]:
                    explored[next_state] = new_cost
                    priority = new_cost + heuristic(next_state)
                    heapq.heappush(frontier, (priority, next_state, path + [(move, next_state)]))

        return None

    def get_successors(self, state):
        def swap(state, i, j):
            state = list(state)
            state[i], state[j] = state[j], state[i]
            return tuple(state)

        moves = []
        empty_index = state.index(0)
        x, y = divmod(empty_index, 3)

        if x > 0:
            moves.append(("Up", swap(state, empty_index, empty_index - 3)))
        if x < 2:
            moves.append(('Down', swap(state, empty_index, empty_index + 3)))
        if y > 0:
            moves.append(('Left', swap(state, empty_index, empty_index - 1)))
        if y < 2:
            moves.append(('Right', swap(state, empty_index, empty_index + 1)))
        return moves

    def solve_puzzle(self, heuristic):
        start_time = time.perf_counter()
        process = psutil.Process()
        start_memory = process.memory_info().rss

        path = self.a_star_search(heuristic)

        end_time = time.perf_counter()
        end_memory = process.memory_info().rss

        if path is None:
            print("No solution found.")
        else:
            print(f"Number of steps: {len(path)}")
            print(f"Elapsed time taken: {end_time - start_time} seconds")
            print(f"Memory consumed: {end_memory - start_memory} bytes")
            print("Path to goal:")
            for move, state in path:
                print(f"Move: {move}, State: {state}")
            print(f"Final state: {self.goal}")

    def is_consistent(self, heuristic):
        def swap(state, i, j):
            state = list(state)
            state[i], state[j] = state[j], state[i]
            return tuple(state)

        def get_successors(state):
            moves = []
            empty_index = state.index(0)
            x, y = divmod(empty_index, 3)

            if x > 0:
                moves.append(swap(state, empty_index, empty_index - 3))
            if x < 2:
                moves.append(swap(state, empty_index, empty_index + 3))
            if y > 0:
                moves.append(swap(state, empty_index, empty_index - 1))
            if y < 2:
                moves.append(swap(state, empty_index, empty_index + 1))
            return moves

        def heuristic_cost(state):
            return heuristic(state)

        # Generate all possible states
        for state in itertools.permutations(range(9)):
            if not self.isSolvable(state):
                continue

            h = heuristic_cost(state)
            for successor in get_successors(state):
                step_cost = 1  # The cost of moving from the current state to a successor is 1
                h_successor = heuristic_cost(successor)
                if h > step_cost + h_successor:
                    print(
                        f"Heuristic is inconsistent: h({state}) = {h} > 1 + h({successor}) = {step_cost} + {h_successor}")
                    return False
        return True


# Usage example
puzzle = Puzzle()
print("Initial state:", puzzle.start)
print("Goal state:", puzzle.goal)

print("\nSolving with Misplaced Tiles Heuristic:")
puzzle.solve_puzzle(puzzle.heuristic_misplaced_tiles)

print("\nSolving with Manhattan Distance Heuristic:")
puzzle.solve_puzzle(puzzle.heuristic_manhattan_distance)

print("\nChecking consistency of Misplaced Tiles Heuristic:")
print("Consistent:", puzzle.is_consistent(puzzle.heuristic_misplaced_tiles))

print("\nChecking consistency of Manhattan Distance Heuristic:")
print("Consistent:", puzzle.is_consistent(puzzle.heuristic_manhattan_distance))
