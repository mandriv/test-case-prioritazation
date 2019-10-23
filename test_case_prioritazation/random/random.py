import time
import math
import random

from ..ga.individual import Individual

def start(tests, config):
    TIME_LIMIT = config['TIME_LIMIT']
    start_time = time.time()
    elapsed = 0
    last_elapsed_time_floored = 0
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
        # Generate new random solution
        new_individual = Individual(None, tests, random.randint(1, len(tests)))
        if new_individual.fitness > individual.fitness:
            individual = new_individual
    # Printing graph of best fitted individual
    print('Top individual found after ' + str(TIME_LIMIT) + 's is:')
    individual.print()
    individual.draw_graphs()
