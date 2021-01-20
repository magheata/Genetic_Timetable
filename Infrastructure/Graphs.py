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
        plt.plot(self.best_ind_evolution)
        plt.xlabel("Iteration")
        plt.ylabel("Individual Cost")
        plt.title("Best individual over iterations " + self.name)
        plt.savefig(f"{Constants.DIR_GRAPH_RESULTS}/{self.folder_name}/{file_name}")
        plt.show(block=False)

    def best_ind_constraints_plot(self, file_name=Constants.GRAPH_CONSTRAINT_EVOLUTION):
        fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(15, 15))
        # Hard constraints
        ax[0, 0].set_title("Hard Const. 1")
        ax[0, 0].plot(np.array(self.best_ind_constraints_evolution['H1']), color='r')
        ax[0, 0].set_xlabel("Iterations")
        ax[0, 0].set_ylabel("Cost")

        ax[0, 1].set_title("Hard Const. 5")
        ax[0, 1].plot(np.array(self.best_ind_constraints_evolution['H5']), color='r')
        ax[0, 1].set_xlabel("Iterations")
        ax[0, 1].set_ylabel("Cost")

        # Soft constraints
        ax[1, 0].set_title("Soft Const. 1")
        ax[1, 0].plot(np.array(self.best_ind_constraints_evolution['S1']), color='g')
        ax[1, 0].set_xlabel("Iterations")
        ax[1, 0].set_ylabel("Cost")

        ax[1, 1].set_title("Soft Const. 2")
        ax[1, 1].plot(np.array(self.best_ind_constraints_evolution['S2']), color='g')
        ax[1, 1].set_xlabel("Iterations")
        ax[1, 1].set_ylabel("Cost")

        ax[2, 0].set_title("Soft Const. 3")
        ax[2, 0].plot(np.array(self.best_ind_constraints_evolution['S3']), color='g')
        ax[2, 0].set_xlabel("Iterations")
        ax[2, 0].set_ylabel("Cost")

        ax[2, 1].set_title("Soft Const. 4")
        ax[2, 1].plot(np.array(self.best_ind_constraints_evolution['S4']), color='g')
        ax[2, 1].set_xlabel("Iterations")
        ax[2, 1].set_ylabel("Cost")

        ax[3, 0].set_title("Soft Const. 5")
        ax[3, 0].plot(np.array(self.best_ind_constraints_evolution['S5']), color='g')
        ax[3, 0].set_xlabel("Iterations")
        ax[3, 0].set_ylabel("Cost")

        ax[3, 1].remove()
        # Set output
        fig.tight_layout()
        fig.savefig(f"{Constants.DIR_GRAPH_RESULTS}/{self.folder_name}/{file_name}")
        plt.show(block=False)
