# -*- coding: utf-8 -*-
# import numpy as np
import os

import matplotlib.pyplot as plt
import numpy as np

import Constants


class Graphs():

    def __init__(self, report_name: str, best_individuals, generation_costs, best_individuals_constraints,
                 folder_name):
        self.name = "(" + report_name + ")"
        self.best_ind_evolution = np.array(best_individuals)
        self.generation_cost_evolution = np.array(generation_costs)
        self.best_ind_constraints_evolution = best_individuals_constraints
        self.folder_name = folder_name
        os.mkdir(f"{Constants.DIR_GRAPH_RESULTS}/{self.folder_name}")

    def generation_cost_plot(self, file_name=Constants.GRAPH_GENERATION):
        plt.figure(1)
        plt.plot(self.generation_cost_evolution)
        plt.xlabel("Iteration")
        plt.ylabel("Generation Cost")
        plt.title("Generation over iterations " + self.name)
        plt.savefig(f"{Constants.DIR_GRAPH_RESULTS}/{self.folder_name}/{file_name}")
        plt.show(block=False)

    def best_ind_plot(self, file_name=Constants.GRAPH_BEST_INDIVIDUAL):
        plt.figure(1)
        axes = plt.gca()
        axes.set_ylim([0,np.max(self.best_ind_evolution)])
        plt.plot(self.best_ind_evolution)
        plt.xlabel("Iteration")
        plt.ylabel("Individual Cost")
        plt.title("Best individual over iterations " + self.name)
        plt.savefig(f"{Constants.DIR_GRAPH_RESULTS}/{self.folder_name}/{file_name}")
        plt.show(block=False)

    def constraints_plot(self, constraint : str, file_name=Constants.GRAPH_CONSTRAINT_EVOLUTION):
        plt.figure(1)
        plt.plot(np.array(self.best_ind_constraints_evolution[constraint]))
        plt.xlabel("Iteration")
        plt.ylabel(f"{constraint} Cost")
        plt.title(f"Best individual's {constraint} over iterations. {self.name}")
        file_name = constraint + file_name
        plt.savefig(f"{Constants.DIR_GRAPH_RESULTS}/{self.folder_name}/{file_name}")
        plt.show(block=False)
