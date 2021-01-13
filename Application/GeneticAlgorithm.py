import Constants
from Application.Chromosome import Chromosome
from Application.Fitness import Fitness
from copy import deepcopy
import random
import pandas as pd
import numpy as np

from Application.TimeTable import TimeTable


class GeneticAlgorithm:

    def __init__(self, courses: dict, classes: dict, teachers: dict):
        self.courses = courses
        self.classes = classes
        self.teachers = teachers
        self.population_size = Constants.POPULATION_SIZE
        self.mutation = 0.95
        self.percentage_of_improvement = 0.3
        self.improvement = 0
        self.fitness = Fitness()

    def find_solution(self):
        chromosomes = []
        computed_generation = 0
        # INITIALISE POPULATION WITH RANDOM CANDIDATE SOLUTION
        for i in range(0, self.population_size):
            chromosome = Chromosome(deepcopy(self.courses),
                                    deepcopy(self.classes),
                                    deepcopy(self.teachers),
                                    computed_generation,
                                    i)
            random_chromosome = chromosome.generate_initial_individual()
            chromosomes.append(random_chromosome)

        # EVALUATE EACH CANDIDATE

        for chromosome in chromosomes:
            # print(f"Generation: {chromosome.generation} individual: {chromosome.idx}")
            chromosome.cost = self.fitness.calculate_fitness(chromosome)
            # chromosome.cost = self.fitness.soft_constraint_8(chromosome)
            # print(f"Cost: {chromosome.cost}\n")

        # REPEAT UNTIL CONDITION IS MET
        while self.improvement < self.percentage_of_improvement and computed_generation <= Constants.MAXIMUM_GENERATIONS:
            # Order the individuals of the previous generation by fitness cost
            cost_individuals = {}
            for individual in chromosomes:
                cost_individuals[individual] = individual.cost

            sorted_generation = {k: v for k, v in
                                 sorted(cost_individuals.items(), key=lambda item: item[1])}

            generation = [individual for individual in sorted_generation]
            # Calculate the old generation's cost to be able to compare if we have improved in
            # the next generation
            old_fitness = sum([individual.cost for individual in generation])
            # SELECT PARENTS
            # coger 4 de los cromosomas con mejor coste y elegir random 2 padres
            parent_1 = generation[0]
            parent_2 = generation[1]
            # print(TimeTable(parent_1.timetable, '1ESO'))
            # print(TimeTable(parent_2.timetable, '1ESO'))
            # RECOMBINATION
            for new_individual in range(0, Constants.DESCENDANTS):
                random_idx_parent1 = random.randint(0, (Constants.TIME_SLOTS - 1))
                random_idx_parent2 = random_idx_parent1
                #print(f"P1: {random_idx_parent1} P2: {random_idx_parent2}")
                new_chromosome_timetable = deepcopy(parent_1.timetable.loc[:, 0:random_idx_parent1])
                parent_2_timetable = deepcopy(
                    parent_1.timetable.loc[:, random_idx_parent2 + 1:Constants.TIME_SLOTS - 1])
                new_chromosome_timetable = pd.concat([new_chromosome_timetable, parent_2_timetable], axis=1)
                #print(new_chromosome_timetable)
                new_chromosome = Chromosome(deepcopy(self.courses),
                                            deepcopy(self.classes),
                                            deepcopy(self.teachers),
                                            computed_generation,
                                            new_individual)
                # Set new chromosome's timetable based on the parents
                new_chromosome.set_timetable(timetable=new_chromosome_timetable)
                new_chromosome.calculate_teachers_availability()
            # MUTATE

            # EVALUATE EACH CANDIDATE

            # SELECT NEXT GENERATION

            # generation = new_generation
            fitness_generation = sum([individual.cost for individual in generation])
            self.improvement = (old_fitness - fitness_generation) / old_fitness
            computed_generation = computed_generation + 1
        # RETURN CHROMOSOME WITH LEAST COST
        return chromosomes[0].timetable
