import time
import math
import random
import copy

from ..ga.individual import Individual
from ..utils import stats

def start(tests, config):
    TIME_LIMIT = config['TIME_LIMIT']
    # always perform operations
    MUTATION_CHANCE = 1.0
    ADDITION_CHANCE = 10
    REMOVAL_CHANCE = 10
    start_time = time.time()
    elapsed = 0
    last_elapsed_time_floored = 0
    iteration_number = 0
    evaluation_graph = stats.Graph()
    # Generate initial solution
    print('Initial random solution:')
    individual = Individual(None, tests, random.randint(1, len(tests)))
    individual.print()
    # hill climbing step
    print('Starting hill climbing algorithm...\n')
    while elapsed < TIME_LIMIT:
        # Print countdown
        elapsed = time.time() - start_time
        current_elapsed_time_floored = math.floor(elapsed)
        if (
            current_elapsed_time_floored != 0 and
            current_elapsed_time_floored != last_elapsed_time_floored and
            current_elapsed_time_floored % 5 == 0
            ):
            print(str(math.ceil(TIME_LIMIT - elapsed)) + 's left, current best solution: ')
            individual.print()
        last_elapsed_time_floored = current_elapsed_time_floored
        # Stats
        evaluation_graph.add_data(iteration_number, individual.fitness)
        # Generate new candidates
        candidates = []
        # original
        individual_copy = copy.copy(individual)
        candidates.append(individual_copy)
        # mutation
        individual_copy = copy.copy(individual)
        individual_copy.mutate(tests, MUTATION_CHANCE)
        candidates.append(individual_copy)
        # adding test
        individual_copy = copy.copy(individual)
        individual_copy.add_test(tests, ADDITION_CHANCE)
        candidates.append(individual_copy)
        # removing test
        individual_copy = copy.copy(individual)
        individual_copy.remove_test(REMOVAL_CHANCE)
        candidates.append(individual_copy)
        # sort candidates by fitness
        candidates.sort(key=lambda individual: individual.fitness, reverse=True)
        # pick best one as new individual
        individual = copy.copy(candidates[0])

        iteration_number += 1
    # Printing graph of best fitted individual
    evaluation_graph.draw_graph('Best fitness individual over iteration', 'Iteration number', 'Fitness')
    print('Top individual found after ' + str(TIME_LIMIT) + 's is:')
    individual.print()
    individual.draw_graphs()
