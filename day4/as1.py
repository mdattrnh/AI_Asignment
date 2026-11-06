import random
from simpleai.search import SearchProblem, genetic
class NQueenGA(SearchProblem):
    def __init__(self, n=8):
        super().__init__(initial_state=None)
        self.n = n
        self.crossover_count = 0
        self.mutation_count = 0

    def generate_random_state(self):
        return tuple(
            random.randint(0, self.n - 1)
            for _ in range(self.n)
        )

    def value(self, state):
        max_pairs = self.n * (self.n - 1) // 2
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                same_row = state[i] == state[j]
                same_diagonal = (
                    abs(state[i] - state[j]) == abs(i - j)
                )

                if same_row or same_diagonal:
                    conflicts += 1
        return max_pairs - conflicts

    def crossover(self, state1, state2):
        cut = random.randint(1, self.n - 1)
        child = state1[:cut] + state2[cut:]
        self.crossover_count += 1
        if self.crossover_count <= 3:
            print("\nLAI GHEP")
            print("CHA 1:", state1)
            print("CHA 2:", state2)
            print("Cut:", cut)
            print("CON:", child)
        return child

    def mutate(self, state):
        new_state = list(state)
        column = random.randint(0, self.n - 1)
        old_row = new_state[column]
        possible_rows = [
            row for row in range(self.n)
            if row != old_row
        ]
        new_state[column] = random.choice(possible_rows)
        mutated = tuple(new_state)
        self.mutation_count += 1
        if self.mutation_count <= 3:
            print("\nDOT BIEN")
            print("TRUOC:", state)
            print("SAU:", mutated)
        return mutated

    def print_board(self, state):
        print("\nBAN CO:")
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if state[col] == row:
                    line += " Q "
                else:
                    line += " . "
            print(line)
        print()

if __name__ == "__main__":
    random.seed(42)
    n = 8
    population_size = 100
    mutation_rate = 0.1
    iterations = 1000
    max_runs = 10

    problem = NQueenGA(n)
    max_fitness = n * (n - 1) // 2

    print("Giai bai toan N-Queens voi n =", n)
    print("Kich thuoc quan the:", population_size)
    print("Ti le dot bien:", mutation_rate)
    print("So lan lap:", iterations)
    print("Fitness toi da:", max_fitness)

    initial = problem.generate_random_state()
    print("\nCau hinh ngau nhien:", initial)
    print("Fitness ban dau:", problem.value(initial))

    best_state = None
    best_fitness = -1

    for run in range(max_runs):
        print("\nChay lan thu", run + 1)

        result = genetic(
            problem,
            population_size=population_size,
            mutation_chance=mutation_rate,
            iterations_limit=iterations
        )

        if result is not None:
            state = result.state
            fitness = problem.value(state)

            print("Ket qua tim duoc:", state)
            print("Fitness:", fitness)

            if fitness > best_fitness:
                best_fitness = fitness
                best_state = state

            if fitness == max_fitness:
                print("Da tim duoc nghiem hop le!")
                break
        else:
            print("Khong tim thay loi giai")

    print("\n------ KET QUA ------")
    print("Cau hinh tot nhat:", best_state)
    print("Fitness:", best_fitness, "/", max_fitness)
    print("So cap hau xung dot:",
          max_fitness - best_fitness)

    print("So lan lai ghep:", problem.crossover_count)
    print("So lan dot bien:", problem.mutation_count)

    if best_state is not None:
        problem.print_board(best_state)

    if best_fitness == max_fitness:
        print("\nTHANH CONG: Khong co hai hau tan cong nhau.")
    else:
        print("\nChua tim duoc nghiem hoan hao.")
