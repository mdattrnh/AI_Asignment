
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    limited_depth_first,
    iterative_limited_depth_first,
    uniform_cost,
    greedy,
    astar
)
INITIAL = (
    (1, 2, 3),
    (4, 0, 6),
    (7, 5, 8)
)
GOAL = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)
class EightPuzzle(SearchProblem):
    def find_empty(self, state):
        for x in range(3):
            for y in range(3):
                if state[x][y] == 0:
                    return x, y
    def actions(self, state):
        x, y = self.find_empty(state)
        directions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }
        valid = []
        for action, (dx, dy) in directions.items():
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                valid.append(action)
        return valid
    def result(self, state, action):
        x, y = self.find_empty(state)

        directions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

        dx, dy = directions[action]

        new_x = x + dx
        new_y = y + dy

        new_state = [list(row) for row in state]

        new_state[x][y], new_state[new_x][new_y] = (
            new_state[new_x][new_y],
            new_state[x][y]
        )

        return tuple(tuple(row) for row in new_state)
    def is_goal(self, state):
        return state == GOAL

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        distance = 0
        for x in range(3):
            for y in range(3):
                number = state[x][y]
                if number == 0:
                    continue
                for goal_x in range(3):
                    for goal_y in range(3):
                        if GOAL[goal_x][goal_y] == number:
                            distance += (
                                abs(x - goal_x)
                                + abs(y - goal_y)
                            )
        return distance
def print_board(state):
    for row in state:
        print(" ".join(
            str(n) if n != 0 else "_"
            for n in row
        ))
    print()
def solve(name, algorithm):
    problem = EightPuzzle(initial_state=INITIAL)

    if name == "DLS":
        result = algorithm(
            problem,
            depth_limit=10,
            graph_search=True
        )
    else:
        result = algorithm(
            problem,
            graph_search=True
        )
    if result is None:
        print("Khong tim thay loi giai")
        return
    print("\nThuat toan:", name)
    print("So buoc:", len(result.path()) - 1)
    print("Chi phi:", result.cost)

    for step, (action, state) in enumerate(result.path()):
        print(f"Buoc {step}: {action or 'START'}")
        print_board(state)
def main():
    algorithms = {
        "1": ("BFS", breadth_first),
        "2": ("DFS", depth_first),
        "3": ("DLS", limited_depth_first),
        "4": ("IDDFS", iterative_limited_depth_first),
        "5": ("UCS", uniform_cost),
        "6": ("Greedy", greedy),
        "7": ("A*", astar)
    }

    print("Trang thai ban dau:")
    print_board(INITIAL)

    print("Trang thai dich:")
    print_board(GOAL)

    for key, (name, _) in algorithms.items():
        print(f"{key}. {name}")

    choice = input("Chon thuat toan (1-7): ")

    if choice in algorithms:
        name, algorithm = algorithms[choice]
        solve(name, algorithm)
    else:
        print("Lua chon khong hop le")

if __name__ == "__main__":
    main()
