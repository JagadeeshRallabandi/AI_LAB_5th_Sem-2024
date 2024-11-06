import random
import time


def fitness(chromosome):
    n = len(chromosome)
    non_attacking_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if chromosome[i] != chromosome[j] and abs(chromosome[i] - chromosome[j]) != abs(i - j):
                non_attacking_pairs += 1
    return non_attacking_pairs


def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(range(len(population)), k)
    selected_fitnesses = [fitnesses[i] for i in selected]
    best_idx = selected[selected_fitnesses.index(max(selected_fitnesses))]
    return population[best_idx]


def crossover(parent1, parent2):
    n = len(parent1)
    crossover_point = random.randint(1, n - 2)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutation(chromosome, mutation_rate=0.05):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(chromosome)), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome


def genetic_algorithm(time_limit, pop_size=100, mutation_rate=0.05):
    start_time = time.time()
    n = 8
    population = [random.sample(range(1, n + 1), n) for _ in range(pop_size)]  # Initialize population
    best_solution = None
    best_fitness = 0

    while time.time() - start_time < time_limit:
        fitnesses = [fitness(ind) for ind in population]
        new_population = []
        for _ in range(pop_size // 2):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            child1, child2 = crossover(parent1, parent2)

            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)

            new_population.append(child1)
            new_population.append(child2)

        population = new_population

        for i, individual in enumerate(population):
            current_fitness = fitness(individual)
            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_solution = individual

        if best_fitness == 28:
            break

    return best_solution, best_fitness


def fitness_binary_matrix(matrix):
    n = len(matrix)
    queens = [(i, row.index(1)) for i, row in enumerate(matrix) if 1 in row]
    non_attacking_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            q1, q2 = queens[i], queens[j]
            if q1[0] != q2[0] and q1[1] != q2[1] and abs(q1[0] - q2[0]) != abs(q1[1] - q2[1]):
                non_attacking_pairs += 1
    return non_attacking_pairs


def generate_binary_matrix():
    matrix = [[0 for _ in range(8)] for _ in range(8)]
    positions = random.sample(range(8), 8)
    for row, col in enumerate(positions):
        matrix[row][col] = 1
    return matrix


def crossover_binary_matrix(parent1, parent2):
    crossover_point = random.randint(1, 7)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutation_binary_matrix(matrix, mutation_rate=0.05):
    if random.random() < mutation_rate:
        i, j = random.sample(range(8), 2)
        matrix[i], matrix[j] = matrix[j], matrix[i]
    return matrix


def genetic_algorithm_binary_matrix(time_limit, pop_size=100, mutation_rate=0.05):
    start_time = time.time()
    population = [generate_binary_matrix() for _ in range(pop_size)]
    best_solution = None
    best_fitness = 0

    while time.time() - start_time < time_limit:
        fitnesses = [fitness_binary_matrix(ind) for ind in population]
        new_population = []
        for _ in range(pop_size // 2):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            child1, child2 = crossover_binary_matrix(parent1, parent2)

            child1 = mutation_binary_matrix(child1, mutation_rate)
            child2 = mutation_binary_matrix(child2, mutation_rate)

            new_population.append(child1)
            new_population.append(child2)

        population = new_population

        for i, individual in enumerate(population):
            current_fitness = fitness_binary_matrix(individual)
            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_solution = individual

        if best_fitness == 28:
            break

    return best_solution, best_fitness


time_limits = [10, 50, 100]  # in seconds

results = []

for t in time_limits:
    result_perm = genetic_algorithm(t)
    result_bin = genetic_algorithm_binary_matrix(t)

    results.append({
        'Time (s)': t,
        'Permutation Representation': result_perm,
        'Binary Matrix Representation': result_bin,
    })

best_overall_solution = None
best_overall_fitness = -1
best_representation = ""

for result in results:
    print(f"Time: {result['Time (s)']} seconds")
    print(
        f"Permutation Representation Best Solution: {result['Permutation Representation'][0]}, Fitness: {result['Permutation Representation'][1]}")
    print(
        f"Binary Matrix Representation Best Solution: {result['Binary Matrix Representation'][0]}, Fitness: {result['Binary Matrix Representation'][1]}")
    print()

    # Check for the best solution across both representations
    if result['Permutation Representation'][1] > best_overall_fitness:
        best_overall_solution = result['Permutation Representation'][0]
        best_overall_fitness = result['Permutation Representation'][1]
        best_representation = "Permutation Representation"

    if result['Binary Matrix Representation'][1] > best_overall_fitness:
        best_overall_solution = result['Binary Matrix Representation'][0]
        best_overall_fitness = result['Binary Matrix Representation'][1]
        best_representation = "Binary Matrix Representation"

print(f"Best Overall Solution comes from: {best_representation}")
print(f"Best Solution: {best_overall_solution}, Fitness: {best_overall_fitness}")
