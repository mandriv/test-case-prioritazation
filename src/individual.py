import random
from matplotlib import pyplot as plt
import numpy as np

class Individual:
    def __init__(self, genes = [], available_tests = [], number_of_tests_to_pick = 0):
        if len(genes) == 0:
            test_pool = available_tests.copy()
            self.genes = []
            for i in range(number_of_tests_to_pick):
                random_index = random.randint(0, len(test_pool) - 1)
                test = test_pool.pop(random_index)
                self.genes.append(test)
        else:
            self.genes = genes
        self.fraction_detected_faults = 0.0
        self.apfd = 0.0
        self.calculate_fitness()

    def to_string(self):
        string = ''
        for gene in self.genes:
            id_len = len(gene['id'])
            formatted_id = gene['id']
            if id_len == 2:
                formatted_id += '  '
            elif id_len == 3:
                formatted_id += ' '
            string += formatted_id + ' - ' + ','.join(str(f) for f in gene['faults']) + '\n'
        string += 'fitness: ' + str(self.fitness) + '\n'
        string += 'APFD: ' + str(self.apfd) + '\n'
        string += 'Detected: ' + str(self.fraction_detected_faults) + '\n'
        return string

    def print(self):
        print(self.to_string())

    def get_number_of_tests(self):
        return len(self.genes)

    def draw_graph_apfd(self):
        plt.title("Percent Detected Faults over Test Suite Fraction")
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
        plt.text(0.4, 10, 'APFD = ' + str(round(self.fitness * 100, 2)) + '%')
        plt.show()

    def calculate_fitness(self):
        # fitness based on APFD from the paper Test Case Prioritization: A Family of Empirical Studies by Elbaum et al.
        # APFD is basically the area under the curve in the graph of a fraction of total tests ran to the fraction of faults detected
        number_of_tests = self.get_number_of_tests()
        # each tests have the same number of faults to detect, so [0] is ok
        number_of_faults = len(self.genes[0]['faults'])
        faults_detected = [0] * number_of_faults
        # curve values
        x = [0.0]
        y = [0.0]
        for i in range(number_of_tests):
            test_faults = self.genes[i]['faults']
            for j in range(len(test_faults)):
                # identified new fault
                if test_faults[j] == 1 and faults_detected[j] == 0:
                    faults_detected[j] = 1
            self.fraction_detected_faults = faults_detected.count(1) / number_of_faults
            fraction_of_tests_completed = (i + 1) / number_of_tests
            x.append(fraction_of_tests_completed)
            y.append(self.fraction_detected_faults)

        self.graph_data = { 'x': x, 'y': y }
        self.apfd = np.trapz(y, x = x)
        APFD_WEIGH = 0.8
        COMPLETENESS_WEIGHT = 0.2
        self.fitness = (APFD_WEIGH * self.apfd) + (COMPLETENESS_WEIGHT * self.fraction_detected_faults)

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

    def mutate(self, available_tests, chance):
        if random.random() >= chance:
            return self
        def filter_existing(test):
            for gene in self.genes:
                return gene['id'] != test['id']

        test_pool = list(filter(filter_existing, available_tests))
        random_gene_index = random.randint(0, self.get_number_of_tests() - 1)
        random_test_index = random.randint(0, len(test_pool) - 1)
        self.genes[random_gene_index] = test_pool[random_test_index]
