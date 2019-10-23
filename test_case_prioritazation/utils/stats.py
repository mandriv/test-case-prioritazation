import random

from matplotlib import pyplot as plt
import numpy as np

class Graph:
    def __init__(self):
        self.x = []
        self.y = []

    def add_data(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def draw_graph(self, title, x_label, y_label):
        # APFD and individual data
        plt.figure()
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(x_label)
        axes = plt.gca()
        axes.set_xlim([0, self.x[-1]])
        axes.set_ylim([self.y[0] - 0.02, self.y[-1]])

        plt.plot(self.x, self.y, marker='.')
        plt.grid()

        plt.draw()
