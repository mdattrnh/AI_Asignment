import random
from simpleai.search import (
    CspProblem,
    backtrack,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
    SearchProblem,
    genetic
)
N = 5

def count_conflicts(state):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            same_row = state[i] == state[j]
            same_diagonal = abs(state[i] - state[j]) == abs(i - j)
            if same_row or same_diagonal:
                conflicts += 1
    return conflicts
def print_board(state):
    if state is None:
        print("Khong tim thay nghiem")
        return
    for row in range(N):
        for col in range(N):
            if state[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
    print("State:", state)
    print("Conflicts:", count_conflicts(state))
#CSP - building
variables = tuple(range(N))
domains = {
    variable: list(range(N))
    for variable in variables
}
def queen_constraint(variables, values):
    col1, col2 = variables
    row1, row2 = values

    if row1 == row2:
        return False

    if abs(row1 - row2) == abs(col1 - col2):
        return False

    return True


constraints = []

for i in range(N):
    for j in range(i + 1, N):
        constraints.append(
            ((i, j), queen_constraint)
        )

csp_problem = CspProblem(
    variables,
    domains,
    constraints
)
#backtracking 
strategies = [
    ("Default", "", ""),
    ("MRV", MOST_CONSTRAINED_VARIABLE, ""),
    ("Degree", HIGHEST_DEGREE_VARIABLE, ""),
    ("LCV", "", LEAST_CONSTRAINING_VALUE),
    ("MRV + LCV",
     MOST_CONSTRAINED_VARIABLE,
     LEAST_CONSTRAINING_VALUE)
]
print("\n-------- CSP BACKTRACKING -------- ")
for name, var_heuristic, val_heuristic in strategies:
    result = backtrack(
        csp_problem,
        variable_heuristic=var_heuristic,
        value_heuristic=val_heuristic,
        inference=False
    )
    print("\nChien luoc:", name)
    if result is not None:
        state = tuple(result[i] for i in range(N))
        print_board(state)
    else:
        print("Khong tim thay nghiem")
class NQueenGA(SearchProblem):
    def __init__(self, n=5):
        super().__init__(initial_state=None)
        self.n = n
        self.crossover_count = 0
        self.mutation_count = 0
    # Sinh ca the ngau nhien
    def generate_random_state(self):
        return tuple(
            random.randint(0, self.n - 1)
            for _ in range(self.n)
        )
    # fitness  
    def value(self, state):
        return 1 + self.n * (self.n - 1) // 2 - count_conflicts(state)
    
    def crossover(self, state1, state2):
        self.crossover_count += 1
        cut = random.randint(1, self.n - 1)
        child = state1[:cut] + state2[cut:]
        return child

    def mutate(self, state):
        self.mutation_count += 1
        new_state = list(state)
        pos = random.randrange(self.n)
        new_state[pos] = random.randint(
            0, self.n - 1
        )
        return tuple(new_state)

print("\n------ GENETIC ALGORITHM -------")
ga_problem = NQueenGA(N)
best = None
for attempt in range(1, 6):
    result = genetic(
        ga_problem,
        population_size=100,
        mutation_chance=0.1,
        iterations_limit=200
    )
    if best is None or result.value > best.value:
        best = result

    print(
        f"Lan {attempt}: "
        f"Fitness = {result.value}, "
        f"State = {result.state}"
    )

    if count_conflicts(best.state) == 0:
        break


print("\nKet qua GA tot nhat:")
print_board(best.state)

print("Fitness:", best.value)
print("So lan crossover:", ga_problem.crossover_count)
print("So lan mutation:", ga_problem.mutation_count)

if count_conflicts(best.state) == 0:
    print("GA tim duoc nghiem hop le!")
else:
    print("GA chua tim duoc nghiem hop le.")
