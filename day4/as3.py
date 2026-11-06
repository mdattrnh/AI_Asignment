from simpleai.search import (
    CspProblem,
    backtrack,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE
)
import time
variables = ('x', 'y')
domains = {
    'x': list(range(-10, 10)),
    'y': list(range(-10, 10))
}
cost_count = 0
def pt1(variables, values):
    global cost_count
    cost_count += 1

    x, y = values
    return 3*x + 2*y == 25

def pt2(variables, values):
    global cost_count
    cost_count += 1

    x, y = values
    return 2*x - y == 5

constraints = [
    (('x', 'y'), pt1),
    (('x', 'y'), pt2)
]
problem = CspProblem(variables, domains, constraints)

def cost(name, variable='', value=''):
    global cost_count
    cost_count = 0
    start = time.perf_counter()
    result = backtrack(
        problem,
        variable_heuristic=variable,
        value_heuristic=value,
        inference=False
    )
    end = time.perf_counter()

    elapsed = (end - start) * 1000
    return {
        'name': name,
        'result': result,
        'cost': cost_count,
        'time': elapsed
    }
results = [
    cost("Default"),
    cost("MRV",
         variable=MOST_CONSTRAINED_VARIABLE),
    cost("Degree",
         variable=HIGHEST_DEGREE_VARIABLE),
    cost("LCV",
         value=LEAST_CONSTRAINING_VALUE),
    cost("MRV + LCV",
         variable=MOST_CONSTRAINED_VARIABLE,
         value=LEAST_CONSTRAINING_VALUE),
    cost("Degree + LCV",
         variable=HIGHEST_DEGREE_VARIABLE,
         value=LEAST_CONSTRAINING_VALUE)
]

print(f"{'Strategy':<18} {'Cost':<12} {'Time (ms)':<15} {'Result'}")
print("-" * 70)

for r in results:
    print(
        f"{r['name']:<18} "
        f"{r['cost']:<12} "
        f"{r['time']:<15.4f} "
        f"{r['result']}"
    )