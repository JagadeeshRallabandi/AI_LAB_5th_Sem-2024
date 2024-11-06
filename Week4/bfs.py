from collections import deque

class MissionariesAndCannibals:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def is_valid_state(self, m_left, c_left, m_right, c_right):
        if m_left < 0 or m_right < 0 or c_left < 0 or c_right < 0:
            return False
        if (c_left > m_left > 0) or (c_right > m_right > 0):
            return False
        return True

    def get_neighbors(self, state):
        m_left, c_left, m_right, c_right, boat_position = state
        neighbors = []

        if boat_position == 0:
            for m in range(3):
                for c in range(3):
                    if (0 < m + c <= 2) and (m <= m_left and c <= c_left):
                        new_m_left = m_left - m
                        new_c_left = c_left - c
                        new_m_right = m_right + m
                        new_c_right = c_right + c
                        if self.is_valid_state(new_m_left, new_c_left, new_m_right, new_c_right):
                            neighbors.append((new_m_left, new_c_left, new_m_right, new_c_right, 1))
        else:
            for m in range(3):
                for c in range(3):
                    if (0 < m + c <= 2) and (m <= m_right and c <= c_right):
                        new_m_left = m_left + m
                        new_c_left = c_left + c
                        new_m_right = m_right - m
                        new_c_right = c_right - c
                        if self.is_valid_state(new_m_left, new_c_left, new_m_right, new_c_right):
                            neighbors.append((new_m_left, new_c_left, new_m_right, new_c_right, 0))

        return neighbors

    def bfs(self):
        open_queue = deque([(self.start, [])])
        closed_set = set()
        closed_set.add(self.start)

        while open_queue:
            current_state, path = open_queue.popleft()

            if current_state == self.goal:
                return path + [current_state]

            for new_state in self.get_neighbors(current_state):
                if new_state not in closed_set:
                    closed_set.add(new_state)
                    open_queue.append((new_state, path + [current_state]))

        return None

    def solve(self):
        path = self.bfs()

        if path is not None:
            print("Solution found:")
            for state in path:
                print(state)
            print(f"The number of moves is {len(path)-1}")
        else:
            print("Solution not found")


if __name__ == "__main__":
    start_state = (3, 3, 0, 0, 0)
    goal_state = (0, 0, 3, 3, 1)

    print("Start State :",start_state)
    print("Goal State :",goal_state)
    print("\n")

    MisAndCan_solver_object = MissionariesAndCannibals(start_state, goal_state)
    MisAndCan_solver_object.solve()