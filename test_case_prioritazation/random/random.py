import time
import math
import random

from ..ga.individual import Individual
from ..utils import stats

def start(tests, config):
    TIME_LIMIT = config['TIME_LIMIT']
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
    print('Starting random algorithm...\n')
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
        # Generate new random solution
        new_individual = Individual(None, tests, random.randint(1, len(tests)))
        if new_individual.fitness > individual.fitness:
            individual = new_individual

        iteration_number += 1
    # Printing graph of best fitted individual
    evaluation_graph.draw_graph('Best fitness individual over iteration', 'Iteration number', 'Fitness')
    print('Top individual found after ' + str(TIME_LIMIT) + 's is:')
    individual.print()
    individual.draw_graphs()
