from collections import deque


class Node:
    def __init__(self, state, action=None, depth=0, path_cost=0, parent=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth


class Puzzle:

    def __init__(self, board):
        self.root = Node(board)

    def display_board(self, board):
        for i in range(len(board)):
            if i != 0 and i % 3 == 0:
                print()
            print(board[i], end=' ')
        print()

    def check_goal_state(self, board):
        return board == [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def solve_bfs(self):
        if self.check_goal_state(self.root):
            return self.find_solution(self.root)

        # Used a double-ended queue to facilitate faster removal from one end of queue
        # and faster insertion at another end
        frontier = deque()
        frontier.append(self.root)
        explored = set()

        while len(frontier) != 0:
            curr_node = frontier.popleft()
            explored.add(tuple(curr_node.state))

            for child_node in self.get_child_nodes(curr_node):
                if self.check_goal_state(curr_node.state):
                    return self.find_solution(curr_node)
                if self.check_solvable(child_node.state) and tuple(child_node.state) not in explored:
                    frontier.append(child_node)

    def solve_dfs(self):
        if self.check_goal_state(self.root):
            return self.find_solution(self.root)

        frontier = []
        frontier.append(self.root)
        explored = set()

        while len(frontier) != 0:
            curr_node = frontier.pop()
            explored.add(tuple(curr_node.state))

            for child_node in self.get_child_nodes(curr_node):
                if self.check_goal_state(curr_node.state):
                    return self.find_solution(curr_node)
                if self.check_solvable(child_node.state) and tuple(child_node.state) not in explored:
                    frontier.append(child_node)

    def get_actions(self, state):
        blank_index = state.index(0)
        actions = []
        if blank_index > 2:
            actions.append('up')
        if blank_index < 6:
            actions.append('down')
        if blank_index % 3 != 0:
            actions.append('left')
        if blank_index % 3 == 0 or blank_index % 3 == 1:
            actions.append('right')
        return actions

    def do_action(self, state, action):
        blank_index = state.index(0)
        if action == 'up':
            state[blank_index - 3], state[blank_index] = state[blank_index], state[blank_index - 3]
        elif action == 'down':
            state[blank_index + 3], state[blank_index] = state[blank_index], state[blank_index + 3]
        elif action == 'left':
            state[blank_index - 1], state[blank_index] = state[blank_index], state[blank_index - 1]
        else:
            state[blank_index + 1], state[blank_index] = state[blank_index], state[blank_index + 1]
        return state

    def get_child_nodes(self, node):
        child_nodes = []
        actions = self.get_actions(node.state)
        for action in actions:
            state_copy = node.state[:]
            state_copy = self.do_action(state_copy, action)
            path_cost = self.get_path_cost(node)
            child_node = Node(state_copy, action, node.depth + 1, path_cost, node)
            child_nodes.append(child_node)

        return child_nodes

    def get_path_cost(self, node):
        final_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        path_cost = node.depth
        for i, j in zip(node.state, final_state):
            if i != j:
                path_cost += 1
        return path_cost

    def check_solvable(self, state) -> bool:
        inversion_count = 0
        for i in range(len(state)):
            if state[i] == 0:
                continue
            for j in range(i + 1, len(state)):
                if state[j] == 0:
                    continue
                if state[i] > state[j]:
                    inversion_count += 1

        if inversion_count % 2 == 0:
            return True
        return False

    def find_solution(self, node):
        print('\nSolution achieved!')
        print(f"Found at depth: {node.depth}\nWith path cost: {node.path_cost}")
        action_list = []
        itr = node
        while itr.parent != None:
            tup = (itr.action, itr.state)
            action_list.append(tup)
            itr = itr.parent

        self.display_board(self.root.state)
        print()
        for i in range(len(action_list) - 1, -1, -1):
            print()
            print(f'Action: {action_list[i][0]}')
            self.display_board(action_list[i][1])


board = [2, 4, 6, 1, 0, 3, 5, 7, 8]
puz = Puzzle(board)
puz.solve_bfs()
puz.solve_dfs()
