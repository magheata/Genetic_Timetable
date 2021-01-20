# -*- coding: utf-8 -*-
from Infrastructure.Graphs import Graphs
from numpy import random as rnd

if __name__ == "__main__":
    best_individual_series = rnd.rand(100)*100
    best_generation_cost = rnd.rand(100)*100
    best_constraints = {}
    best_constraints["H1"] = rnd.rand(100)*100
    best_constraints["H5"] = rnd.rand(100)*100
    best_constraints["S1"] = rnd.rand(100)*10
    best_constraints["S2"] = rnd.rand(100)*10
    best_constraints["S3"] = rnd.rand(100)*10
    best_constraints["S4"] = rnd.rand(100)*10
    best_constraints["S5"] = rnd.rand(100)*10
    
    visualizer = Graphs("Test Report", best_individual_series, best_individual_series, best_constraints)
    visualizer.generation_cost_plot()
    visualizer.best_ind_plot()
    visualizer.best_ind_constraints_plot()
