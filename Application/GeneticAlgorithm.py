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
        self.mutation = 0.8
        self.percentage_of_improvement = 0.05
        self.improvement = 1
        self.fitness = Fitness()

    def generate_individual(self, parent1, parent2, generation, individual):
        parent1_number_of_courses = random.randint(0, len(Constants.COURSES) - 1)
        parent1_courses = random.sample(Constants.COURSES, parent1_number_of_courses)
        parent2_courses = np.setdiff1d(Constants.COURSES, parent1_courses)
        # print(f"P1: {parent1_courses} P2: {parent2_courses}")
        new_chromosome_timetable = deepcopy(parent1.timetable.loc[parent1_courses])
        parent2_timetable = deepcopy(parent2.timetable.loc[parent2_courses])

        new_chromosome_timetable = pd.concat([new_chromosome_timetable, parent2_timetable])
        # print(new_chromosome_timetable)
        new_chromosome = Chromosome(deepcopy(self.courses),
                                    deepcopy(self.classes),
                                    deepcopy(self.teachers),
                                    generation,
                                    individual)
        # Set new chromosome's timetable based on the parents
        new_chromosome.set_timetable(timetable=new_chromosome_timetable)
        new_chromosome.calculate_teachers_availability()
        return new_chromosome

    def order_generation_by_cost(self, chromosomes):
        cost_individuals = {}
        for individual in chromosomes:
            cost_individuals[individual] = individual.cost
        sorted_generation = {k: v for k, v in
                             sorted(cost_individuals.items(), key=lambda item: item[1])}
        return [individual for individual in sorted_generation]

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
            # print(f"Cost: {chromosome.cost}\nConstraints cost: {chromosome.cost_constraints}\n")

        computed_generation += 1

        generated_individuals = deepcopy(chromosomes)
        generation = self.order_generation_by_cost(generated_individuals)
        # REPEAT UNTIL CONDITION IS MET
        while self.improvement > self.percentage_of_improvement and computed_generation <= Constants.MAXIMUM_GENERATIONS:
            print("______________________________")
            # Order the individuals of the previous generation by fitness cost
            #generation = self.order_generation_by_cost(generated_individuals)
            # Calculate the old generation's cost to be able to compare if we have improved in
            # the next generation
            old_fitness = sum([individual.cost for individual in generation])
            # SELECT PARENTS
            parent_options = list(generation[i] for i in range(0, Constants.TOTAL_PARENTS))

            generated_individuals = []
            parents = []
            individual_idx = 0

            for offspring in range(0, int(Constants.TOTAL_PARENTS/2)):
                parent1 = parent_options[random.randint(0, Constants.TOTAL_PARENTS - 1)]
                parent2 = parent_options[random.randint(0, Constants.TOTAL_PARENTS - 1)]
                while parent1 == parent2:
                    parent2 = parent_options[random.randint(0, Constants.TOTAL_PARENTS - 1)]
                if parent1 not in parents:
                    parents.append(parent1)
                if parent2 not in parents:
                    parents.append(parent2)
                print(f"Parent1 cost: {parent1.cost} generation: {parent1.generation} individual: {parent1.idx}\n"
                      f"Parent2 cost: {parent2.cost} generation: {parent2.generation} individual: {parent2.idx}\n")
                # RECOMBINATION
                for new_individual in range(0, Constants.DESCENDANTS - 2):
                    generated_individuals.append(self.generate_individual(parent1,
                                                                          parent2,
                                                                          computed_generation,
                                                                          individual_idx))
                    individual_idx += 1
            # MUTATE
            for individual in generated_individuals:
                mutation_probability = random.random()
                # Mutate individual
                if mutation_probability <= self.mutation:
                    course_to_mutate = random.sample(Constants.COURSES, 1)
                    total_mutations = random.randint(1, 2)
                    for mutation in range(0, total_mutations):
                        course_to_mutate_timetable = individual.timetable.loc[course_to_mutate, :]
                        first_time_slot_to_mutate = random.randint(0, individual.timetable.shape[1] - 1)
                        second_time_slot_to_mutate = random.randint(0, individual.timetable.shape[1] - 1)
                        # Check if both slots are equal
                        while first_time_slot_to_mutate == second_time_slot_to_mutate:
                            second_time_slot_to_mutate = random.randint(0, individual.timetable.shape[1] - 1)
                        first_lesson_to_mutate = deepcopy(course_to_mutate_timetable[first_time_slot_to_mutate])
                        second_lesson_to_mutate = deepcopy(course_to_mutate_timetable[second_time_slot_to_mutate])

                        '''
                        print(f"Before mutation: \nTime Slot 1: {course_to_mutate_timetable[first_time_slot_to_mutate]} \n"
                              f"Time Slot 2: {course_to_mutate_timetable[second_time_slot_to_mutate]}")

                        print(f"First time slot: {first_time_slot_to_mutate} lesson: {first_lesson_to_mutate}")
                        print(f"Second time slot: {second_time_slot_to_mutate} lesson: {second_lesson_to_mutate}")
                        '''

                        course_to_mutate_timetable[first_time_slot_to_mutate] = second_lesson_to_mutate
                        course_to_mutate_timetable[second_time_slot_to_mutate] = first_lesson_to_mutate
                        '''
                        print(f"After mutation: \nTime Slot 1: {course_to_mutate_timetable[first_time_slot_to_mutate]} \n"
                              f"Time Slot 2: {course_to_mutate_timetable[second_time_slot_to_mutate]}\n")
                        '''
            # EVALUATE EACH CANDIDATE
            for individual in generated_individuals:
                individual.cost = self.fitness.calculate_fitness(individual)
                #print(f"Cost: {individual.cost}\nConstraints cost: {individual.cost_constraints}\n")

            # SELECT NEXT GENERATION
            generated_individuals = generated_individuals + parents
            new_generation = deepcopy(self.order_generation_by_cost(generated_individuals))
            generation = list(new_generation[i] for i in range(0, Constants.POPULATION_SIZE))
            fitness_generation = sum([individual.cost for individual in generation])
            print(f"Best individual: {generation[0].cost} generation: {generation[0].generation} individual: {generation[0].idx}\n"
                  f"Fitness generation: {fitness_generation}\n")
            self.improvement = (old_fitness - fitness_generation) / old_fitness
            computed_generation += 1
        # RETURN CHROMOSOME WITH LEAST COST
        return generation[0].timetable
