import random

# roulette wheel selection ruturning individual and its index
def roulette_wheel_selection(individuals):
    max = sum(individual.fitness for individual in individuals)
    pick = random.uniform(0, max)
    current = 0
    for i in range(len(individuals)):
        current += individuals[i].fitness
        if current > pick:
            return [individuals[i], i]
