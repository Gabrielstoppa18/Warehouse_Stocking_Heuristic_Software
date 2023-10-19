import random

# Função de avaliação: f(x) = x^2
def fitness_function(x):
    return x ** 2

# Função para criar uma população inicial de cromossomos
def create_population(size):
    population = []
    for _ in range(size):
        chromosome = random.uniform(-10, 10)  # Intervalo de valores para x
        population.append(chromosome)
    return population

# Função para avaliar a aptidão (fitness) de cada cromossomo na população
def evaluate_population(population):
    fitness_scores = []
    for chromosome in population:
        fitness_scores.append(fitness_function(chromosome))
    return fitness_scores

# Função para selecionar pais com base na roleta viciada (seleção proporcional à aptidão)
def select_parents(population, fitness_scores, num_parents):
    selected_parents = []
    total_fitness = sum(fitness_scores)
    probabilities = [fitness / total_fitness for fitness in fitness_scores]
    
    for _ in range(num_parents):
        selected_index = random.choices(range(len(population)), probabilities)[0]
        selected_parents.append(population[selected_index])
    
    return selected_parents

# Função para realizar crossover de dois pais e gerar filhos
def crossover(parent1, parent2):
    child1 = (parent1 + parent2) / 2  # Simplesmente tira a média dos pais
    child2 = child1  # Para manter o número de cromossomos constante
    return child1, child2

# Função para realizar mutação em um cromossomo
def mutate(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        mutation_amount = random.uniform(-0.1, 0.1)  # Quantidade de mutação
        chromosome += mutation_amount
    return chromosome

# Algoritmo genético
def genetic_algorithm(population_size, num_generations, mutation_rate, num_parents):
    population = create_population(population_size)
    
    for generation in range(num_generations):
        fitness_scores = evaluate_population(population)
        parents = select_parents(population, fitness_scores, num_parents)
        
        next_generation = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            
            child1, child2 = crossover(parent1, parent2)
            
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            next_generation.extend([child1, child2])
        
        population = next_generation
    
    best_solution = min(population, key=lambda x: fitness_function(x))
    best_fitness = fitness_function(best_solution)
    return best_solution, best_fitness

# Parâmetros do algoritmo genético
population_size = 100
num_generations = 50
mutation_rate = 0.1
num_parents = 50

# Execução do algoritmo genético
best_solution, best_fitness = genetic_algorithm(population_size, num_generations, mutation_rate, num_parents)

print("Melhor solução encontrada:", best_solution)
print("Melhor valor de aptidão:", best_fitness)
