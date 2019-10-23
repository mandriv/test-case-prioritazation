import random

from matplotlib import pyplot as plt
import numpy as np

class Individual:
    def __init__(self, genes = None, available_tests = None, number_of_tests_to_pick = None):
        self.genes = []

        if genes is not None:
            self.genes = genes.copy()
        else:
            test_pool = available_tests.copy()
            for i in range(number_of_tests_to_pick):
                random_index = random.randint(0, len(test_pool) - 1)
                test = test_pool.pop(random_index)
                self.genes.append(test)

        self.fitness = 0.0
        self.completeness = 0.0
        self.performance = 0.0
        self.apfd = 0.0
        self.steps_to_plateau = 0
        self.repeating_steps = 0
        self.apfd_to_plateau = 0.0
        self.calculate_fitness()

    def to_string(self):
        string = ''
        string += 'Fitness:\t' + str(self.fitness) + '\n'
        string += 'Completeness:\t' + str(self.completeness) + '\n'
        string += 'Performance:\t' + str(self.performance) + '\n'
        string += 'APFD:\t\t' + str(self.apfd) + '\n'
        string += 'Local APFD:\t' + str(self.apfd_to_plateau) + '\n'
        string += 'No of tests: ' + str(self.get_number_of_tests()) + '\n'
        return string

    def print(self):
        print(self.to_string())

    def print_comparison(self, comparer):
        def get_change_str(val1, val2):
            change = val1 - val2
            change_str = '{:.20f}'.format(change)
            string = ('+', '')[change < 0]
            string += change_str
            return string

        string = ''
        string += 'Fitness:\t' + '{:.20f}'.format(self.fitness)
        string += ' (' + get_change_str(self.fitness, comparer.fitness) + ')\n'
        string += 'Completeness:\t' + '{:.20f}'.format(self.completeness)
        string += ' (' + get_change_str(self.completeness, comparer.completeness) + ')\n'
        string += 'Performance:\t' + '{:.20f}'.format(self.performance)
        string += ' (' + get_change_str(self.performance, comparer.performance) + ')\n'
        string += 'APFD:\t\t' + '{:.20f}'.format(self.apfd)
        string += ' (' + get_change_str(self.apfd, comparer.apfd) + ')\n'
        string += 'Local APFD:\t' + '{:.20f}'.format(self.apfd_to_plateau)
        string += ' (' + get_change_str(self.apfd_to_plateau, comparer.apfd_to_plateau) + ')\n'
        string += 'No of tests:\t' + str(self.get_number_of_tests())
        string += ' (' + get_change_str(self.get_number_of_tests(), comparer.get_number_of_tests()) + ')\n'
        print(string)

    def get_number_of_tests(self):
        return len(self.genes)

    def draw_graphs(self):
        # APFD and individual data
        plt.figure()
        plt.title("Fittest individual:\nPercent Detected Faults over all Test Suite Fractions")
        plt.xlabel("Test Suite Fraction")
        plt.ylabel("Percent Detected Faults")
        axes = plt.gca()
        axes.set_xlim([0.0, 1.0])
        axes.set_ylim([0, 100])

        x = self.graph_data['x']
        y = [i * 100 for i in self.graph_data['y']]
        plt.plot(x, y, marker='.')
        plt.fill_between(x, 0, y, alpha=0.5)
        plt.grid()
        plt.text(0.5, 40, 'Fitness: ' + str(round(self.fitness * 100, 2)) + '%')
        plt.text(0.5, 30, 'Completeness: ' + str(round(self.completeness * 100, 2)) + '%')
        plt.text(0.5, 20, 'Performance: ' + str(round(self.performance * 100, 2)) + '%')
        plt.text(0.5, 10, 'APFD: ' + str(round(self.apfd * 100, 2)) + '%')
        plt.draw()

        plt.figure()
        plt.title("Fittest individual:\nPerformance of the solution")
        plt.xlabel("Test Number")
        plt.ylabel("Percent Detected Faults")
        # Performance
        x = []
        y = []
        for i in range(self.steps_to_plateau + 1):
            x.append(i)
            y.append(self.graph_data['y'][i] * 100)

        axes = plt.gca()
        axes.set_xlim([0, self.steps_to_plateau])
        axes.set_ylim([0, 100])
        plt.plot(x, y, marker='.')
        plt.fill_between(x, 0, y, alpha=0.5)
        plt.grid()
        plt.text(round(self.steps_to_plateau / 3), 40, 'Performance: ' + str(round(self.performance * 100, 2)) + '%')
        plt.text(round(self.steps_to_plateau / 3), 30, 'Number of tests to reach plateau: ' + str(self.steps_to_plateau))
        plt.text(round(self.steps_to_plateau / 3), 20, 'Number of repeating tests on the way: ' + str(self.repeating_steps))
        plt.text(round(self.steps_to_plateau / 3), 10, 'APFD to plateau: ' + str(round(self.apfd_to_plateau * 100, 2)) + '%')
        plt.draw()

        plt.show()

    # mutates fitness field of the object
    # fitness is based on 4 weighted parameters:
    # 1. Fraction of faults detected - completeness
    # 2. Fraction of repeating tests to all tests needed to reach plateau and local apfd - performance
    # 3. Total AFPD
    # 4. APFD to plateau
    def calculate_fitness(self):
        number_of_tests = self.get_number_of_tests()
        # each tests have the same number of faults to detect, so [0] is ok
        number_of_faults = len(self.genes[0]['faults'])
        faults_detected = [0] * number_of_faults
        # get curve values, calculate fraction of tests completed
        x = [0.0]
        y = [0.0]
        for i in range(number_of_tests):
            test_faults = self.genes[i]['faults']
            for j in range(len(test_faults)):
                # identified new fault
                if test_faults[j] == 1 and faults_detected[j] == 0:
                    faults_detected[j] = 1
            self.completeness = faults_detected.count(1) / number_of_faults
            fraction_of_tests_completed = (i + 1) / number_of_tests
            x.append(fraction_of_tests_completed)
            y.append(self.completeness)

        self.graph_data = { 'x': x, 'y': y }
        # calculate performance
        self.steps_to_plateau = 0
        self.repeating_steps = 0
        for i in range(1, len(y)):
            if y[i - 1] == y[i]:
                self.repeating_steps += 1
            self.steps_to_plateau += 1
            if y[i] == self.completeness:
                break
        # less repeating steps = better
        self.performance = (self.steps_to_plateau - self.repeating_steps) / self.steps_to_plateau;
        # modified version of APFD from he paper
        # Test Case Prioritization: A Family of Empirical Studies by Elbaum et al.
        # calculate apfd based on the integral (trapz method)
        # it works if not reached 100% correctness
        # calculate total apfd
        self.apfd = np.trapz(y, x = x)
        # calculate local apfd to the plateau
        local_x = []
        for i in range(self.steps_to_plateau + 1):
            local_x.append(i / self.steps_to_plateau)
        local_y = y[:self.steps_to_plateau + 1]
        self.apfd_to_plateau = np.trapz(local_y, x = local_x)
        # fitness is weighted sum
        COMPLETENESS_WEIGHT = 0.8
        PERFORMANCE_WEIGHT = 0.1
        TOTAL_APFD_WEIGHT = (0.00, 0.01)[self.performance == 1.0]
        LOCAL_APFD_WEIGHT = (0.1, 0.09)[self.performance == 1.0]
        self.fitness = (COMPLETENESS_WEIGHT * self.completeness) + \
            (PERFORMANCE_WEIGHT * self.performance) + \
            (TOTAL_APFD_WEIGHT * self.apfd) + \
            (LOCAL_APFD_WEIGHT * self.apfd_to_plateau)
    # applies crossover with another individual and returns genes of two children
    # if crossover is unsuccessful, return parents genes
    def get_genes_after_crossover(self, second_individual, chance):
        self_number_of_tests = self.get_number_of_tests()
        second_individual_number_of_tests = second_individual.get_number_of_tests()
        enough_tests_for_crossover = self_number_of_tests >= 3 and second_individual_number_of_tests >= 3
        if not enough_tests_for_crossover or random.random() >= chance:
            return [self.genes, second_individual.genes]
        min_number = min(self_number_of_tests, second_individual_number_of_tests)
        max_number = max(self_number_of_tests, second_individual_number_of_tests)
        crossover_index = random.randint(0, min_number - 2)
        genes_child_one = []
        for i in range(second_individual_number_of_tests):
            if i <= crossover_index:
                genes_child_one.append(self.genes[i])
            else:
                genes_child_one.append(second_individual.genes[i])
        genes_child_two = []
        for i in range(self_number_of_tests):
            if i <= crossover_index:
                genes_child_two.append(second_individual.genes[i])
            else:
                genes_child_two.append(self.genes[i])

        return [genes_child_one, genes_child_two]

    # replaces test at random index with a random test
    # returns boolean based on whether or not it succeeded
    def mutate(self, available_tests, chance):
        if random.random() >= chance:
            return False
        def filter_existing(test):
            for gene in self.genes:
                return gene['id'] != test['id']

        test_pool = list(filter(filter_existing, available_tests))
        random_gene_index = random.randint(0, self.get_number_of_tests() - 1)
        random_test_index = random.randint(0, len(test_pool) - 1)
        self.genes[random_gene_index] = test_pool[random_test_index]
        return True

    # adds random tests at random index
    # returns boolean based on whether or not it succeeded
    def add_test(self, available_tests, chance):
        if self.get_number_of_tests() == len(available_tests) or random.random() >= chance:
            return False
        # remove existing tests from available test pool
        test_pool = []
        for test in available_tests:
            index = -1
            for i in range(self.get_number_of_tests()):
                if test['id'] == self.genes[i]['id']:
                    index = i
                    break
            if index == -1:
                test_pool.append(test)

        random_gene_index = random.randint(0, self.get_number_of_tests() - 1)
        random_test_index = random.randint(0, len(test_pool) - 1)
        self.genes.insert(random_gene_index, test_pool[random_test_index])
        return True

    # removes test at random index
    # returns boolean based on whether or not it succeeded
    def remove_test(self, chance):
        if self.get_number_of_tests() == 1 or random.random() >= chance:
            return False

        random_gene_index = random.randint(0, self.get_number_of_tests() - 1)
        self.genes.pop(random_gene_index)
        return True
