import random
from .individual import Individual

INITIAL_NUMBER_OF_TESTS = 15
POPULATION_SIZE = 250
NUMBER_OF_ITERATIONS = 500
ELITES_SIZE = 2
CROSSOVER_CHANCE = 0.2
MUTATION_CHANCE = 0.1

# To-do
'''
- adding and deleting tests based on chance
'''
# Questions
'''
- fitness function - can I make it any better?
- best values - especially initial number of tests and end condidtion
- should we aim to get all the 255 tests in the individual or highest fitness value?
'''

def get_test_data(filename):
    file = open('data/' + filename, 'r')
    lines = file.readlines()
    data = []
    for line in lines:
        # csv
        bits = line.split(',')
        # first thing in csv is an identifier
        id = bits.pop(0)
        # rest are tests
        for i in range(len(bits)):
            # format each bit so it is a int
            bits[i] = int(bits[i][0])
        # create dict that holds identifier and faults detected
        piece = {
            'id': id,
            'faults': bits
        }
        data.append(piece)
    return data

def roulette_wheel_selection(individuals):
    max = sum(individual.fitness for individual in individuals)
    pick = random.uniform(0, max)
    current = 0
    for i in range(len(individuals)):
        current += individuals[i].fitness
        if current > pick:
            return [individuals[i], i]


def main():
    tests = get_test_data('smallfaultmatrix.txt')
    population = []
    best_fitness = 0.0
    # generate random population
    for _ in range(POPULATION_SIZE):
        individual = Individual([], tests, INITIAL_NUMBER_OF_TESTS)
        population.append(individual)
    # ga step
    for i in range(NUMBER_OF_ITERATIONS):
        # Sort generation by fitness
        population.sort(key=lambda individual: individual.fitness, reverse=True)
        if (population[0].fitness > best_fitness):
            print('New best fitness in population ' + str(i) + '!')
            population[0].print()
            best_fitness = population[0].fitness
        # prepare new population, apply elitism
        new_population = population[:ELITES_SIZE]
        # create offspring
        while (len(new_population) != POPULATION_SIZE):
            [parent_one, index_to_remove] = roulette_wheel_selection(population)
            # dont pick same parent twice
            population_without_parent_one = [x for i,x in enumerate(population) if i != index_to_remove]
            [parent_two, _] = roulette_wheel_selection(population_without_parent_one)
            # crossover
            [child_one_genes, child_two_genes] = parent_one.get_genes_after_crossover(parent_two, CROSSOVER_CHANCE)
            child_one = Individual(child_one_genes)
            child_two = Individual(child_two_genes)
            child_one.mutate(tests, MUTATION_CHANCE)
            child_two.mutate(tests, MUTATION_CHANCE)
            new_population.append(child_one)
            new_population.append(child_two)
        population = new_population
    population[0].draw_graph_apfd()


if __name__ == '__main__':
    main()
