import time
import math

from .individual import Individual
from .utils import roulette_wheel_selection

# To-do
'''
- adding and deleting tests based on chance
'''

def start(tests, config):
    # config
    INITIAL_NUMBER_OF_TESTS = config['INITIAL_NUMBER_OF_TESTS']
    POPULATION_SIZE = config['POPULATION_SIZE']
    TIME_LIMIT = config['TIME_LIMIT']
    ELITES_SIZE = config['ELITES_SIZE']
    CROSSOVER_CHANCE = config['CROSSOVER_CHANCE']
    MUTATION_CHANCE = config['MUTATION_CHANCE']
    ADDITION_CHANCE = config['ADDITION_CHANCE']
    REMOVAL_CHANCE = config['REMOVAL_CHANCE']
    # initial values
    population = []
    best_individual = None
    generation_number = 0
    start_time = time.time()
    elapsed = 0
    last_elapsed_time_floored = 0
    print('Creating random population 0...')
    # generate random population
    for _ in range(POPULATION_SIZE):
        individual = Individual(None, tests, INITIAL_NUMBER_OF_TESTS)
        population.append(individual)
    # ga step
    print('Starting genetic algorithm...\n')
    while elapsed < TIME_LIMIT:
        # Print countdown
        elapsed = time.time() - start_time
        current_elapsed_time_floored = math.floor(elapsed)
        if (
            current_elapsed_time_floored != 0 and
            current_elapsed_time_floored != last_elapsed_time_floored and
            current_elapsed_time_floored % 5 == 0
            ):
            print('===============')
            print(
                str(math.ceil(TIME_LIMIT - elapsed)) +
                's left, current generation: ' +
                str(generation_number)
                )
            print('===============\n')
        last_elapsed_time_floored = current_elapsed_time_floored
        # Sort generation by fitness
        population.sort(key=lambda individual: individual.fitness, reverse=True)
        if generation_number == 0:
            best_individual = Individual(population[0].genes)
            print('Fittest individual in generation 0:')
            best_individual.print()
        # Helper printing when finding new best fitness
        if (population[0].fitness > best_individual.fitness):
            print('New fittest individual found in population ' + str(generation_number) + '!')
            population[0].print_comparison(best_individual)
            best_individual = Individual(population[0].genes)
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
            # mutation
            child_one.mutate(tests, MUTATION_CHANCE)
            child_two.mutate(tests, MUTATION_CHANCE)
            # adding test
            child_one.add_test(tests, ADDITION_CHANCE)
            child_two.add_test(tests, ADDITION_CHANCE)
            # removing test
            child_one.remove_test(REMOVAL_CHANCE)
            child_two.remove_test(REMOVAL_CHANCE)
            # add children to new population
            new_population.append(child_one)
            new_population.append(child_two)
        # replace old population with the new one
        population = new_population
        generation_number += 1
    # Printing graph of best fitted individual
    print('Top individual found after ' + str(TIME_LIMIT) + 's is:')
    population[0].print()
    population[0].draw_graphs()
