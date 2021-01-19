import Constants
from Application.Chromosome import Chromosome
from Application.Fitness import Fitness
from copy import deepcopy
import random
import pandas as pd
import numpy as np


class GeneticAlgorithm:

    def __init__(self, courses: dict, classes: dict, teachers: dict):
        self.courses = courses
        self.classes = classes
        self.teachers = teachers
        self.population_size = Constants.POPULATION_SIZE
        self.mutation = 0.15
        self.percentage_of_improvement = 0.0001
        self.improvement = 1
        self.fitness = Fitness()

    def generate_individual(self, parent1, parent2, generation, individual):
        parent1_number_of_courses = random.randint(0, len(Constants.COURSES) - 1)
        parent1_courses = random.sample(Constants.COURSES, parent1_number_of_courses)
        parent2_courses = np.setdiff1d(Constants.COURSES, parent1_courses)
        new_chromosome_timetable = deepcopy(parent1.timetable.loc[parent1_courses])
        parent2_timetable = deepcopy(parent2.timetable.loc[parent2_courses])

        new_chromosome_timetable = pd.concat([new_chromosome_timetable, parent2_timetable])
        new_chromosome = Chromosome(deepcopy(self.courses),
                                    deepcopy(self.classes),
                                    deepcopy(self.teachers),
                                    generation,
                                    individual)
        # Set new chromosome's timetable based on the parents
        new_chromosome.set_timetable(timetable=new_chromosome_timetable)
        new_chromosome.calculate_teachers_availability()
        return new_chromosome

    def generate_initial_population(self, generation):
        chromosomes = []
        # INITIALISE POPULATION WITH RANDOM CANDIDATE SOLUTION
        for i in range(0, self.population_size):
            chromosome = Chromosome(deepcopy(self.courses),
                                    deepcopy(self.classes),
                                    deepcopy(self.teachers),
                                    generation,
                                    i)
            random_chromosome = chromosome.generate_initial_individual()
            chromosomes.append(random_chromosome)

        # EVALUATE EACH CANDIDATE
        for chromosome in chromosomes:
            chromosome.cost = self.fitness.calculate_fitness(chromosome)
        return chromosomes

    def generate_offsprings(self, parent_options, generation):
        generated_individuals = []
        parents = []
        individual_idx = 0
        # Hacer padres monógamos
        for offspring in range(0, int(Constants.TOTAL_PARENTS / 2)):
            parent1 = parent_options[random.randint(0, Constants.TOTAL_PARENTS - 1)]
            if parent1 in parents:
                parent1 = parent_options[random.randint(0, Constants.TOTAL_PARENTS - 1)]
            parent2 = parent_options[random.randint(0, Constants.TOTAL_PARENTS - 1)]
            while parent1 == parent2 and parent2 in parents:
                parent2 = parent_options[random.randint(0, Constants.TOTAL_PARENTS - 1)]
            # if parent1 not in parents:
            parents.append(parent1)
            # if parent2 not in parents:
            parents.append(parent2)
            '''
            parent1 = parent_options[random.randint(0, len(parent_options) - 1)]
            parent2 = parent_options[random.randint(0, len(parent_options) - 1)]
            while parent1 == parent2:
                parent2 = parent_options[random.randint(0, len(parent_options) - 1)]
            parents.append(parent1)
            parents.append(parent2)
            parent_options.remove(parent1)
            parent_options.remove(parent2)
            '''
            print(f"Parent1 cost: {parent1.cost} generation: {parent1.generation} individual: {parent1.idx} "
                  f"constraints: {parent1.cost_constraints}\n"
                  f"Parent2 cost: {parent2.cost} generation: {parent2.generation} individual: {parent2.idx} "
                  f"constraints: {parent2.cost_constraints}\n ")
            for new_individual in range(0, Constants.DESCENDANTS):
                generated_individuals.append(self.generate_individual(parent1,
                                                                      parent2,
                                                                      generation,
                                                                      individual_idx))
                individual_idx += 1
        return generated_individuals, parents

    def mutate_offsprings(self, individuals):
        for individual in individuals:
            mutation_probability = random.random()  # 0 - 1
            # Mutate individual
            if mutation_probability <= self.mutation:
                total_courses_to_mutate = random.randint(1, len(Constants.COURSES) - 1)
                course_to_mutate = random.sample(Constants.COURSES, total_courses_to_mutate)
                for course in course_to_mutate:
                    total_mutations = random.randint(1, 3)  # cambiar menos slots
                    for mutation in range(0, total_mutations):
                        # course_to_mutate_timetable = individual.timetable.loc[course_to_mutate, :]
                        first_time_slot_to_mutate = random.randint(0, Constants.TIME_SLOTS - 1)
                        second_time_slot_to_mutate = random.randint(0, Constants.TIME_SLOTS - 1)
                        # Check if both slots are equal
                        while first_time_slot_to_mutate == second_time_slot_to_mutate:
                            second_time_slot_to_mutate = random.randint(0, Constants.TIME_SLOTS - 1)
                        first_lesson_to_mutate = deepcopy(individual.timetable.loc[course, first_time_slot_to_mutate])
                        second_lesson_to_mutate = deepcopy(individual.timetable.loc[course, second_time_slot_to_mutate])
                        if first_lesson_to_mutate != 0:
                            first_lesson_to_mutate.time_slot = second_time_slot_to_mutate
                        if second_lesson_to_mutate != 0:
                            second_lesson_to_mutate.time_slot = first_time_slot_to_mutate
                        individual.timetable.loc[course, first_time_slot_to_mutate] = second_lesson_to_mutate
                        individual.timetable.loc[course, second_time_slot_to_mutate] = first_lesson_to_mutate

    @staticmethod
    def order_generation_by_cost(chromosomes):
        cost_individuals = {}
        for individual in chromosomes:
            cost_individuals[individual] = individual.cost
        sorted_generation = {k: v for k, v in
                             sorted(cost_individuals.items(), key=lambda item: item[1])}
        return [individual for individual in sorted_generation]

    @staticmethod
    def choose_next_generation(generation):
        new_generation = []
        for p in range(0, Constants.POPULATION_SIZE - 1):
            if generation[p].cost != generation[p - 1].cost:
                if len(new_generation) < Constants.POPULATION_SIZE:
                    new_generation.append(generation[p])
                else:
                    break
        print(len(new_generation))
        return new_generation

    @staticmethod
    def choose_parents_roulette(generation, old_fitness):
        list_percentages = []
        for individual in generation:
            percentage_ind = (old_fitness - individual.cost) / old_fitness
            list_percentages.append(percentage_ind)
        list_percentages = np.cumsum(list_percentages) / (Constants.POPULATION_SIZE - 1)

        parent_options = []
        for i in range(0, Constants.POPULATION_SIZE):
            random_i = random.random()
            idx_bigger_value = np.where(list_percentages > random_i)
            for idx in idx_bigger_value:
                parent_options.append(generation[idx[0]])
        return parent_options

    def choose_parents_tournament(self, generation):
        current_member = 0
        parent_options = []
        k = 5
        while current_member != Constants.TOTAL_PARENTS:
            random_individuals = random.sample(generation, k)
            ordered_individuals = self.order_generation_by_cost(random_individuals)
            parent_options.append(ordered_individuals[0])
            current_member += 1
        return parent_options

    @staticmethod
    def get_costs_generation(generation, best_individual_cost_evolution, best_individual_constraints_evolution,
                             generation_cost_evolution):
        fitness_generation = sum([individual.cost for individual in generation])
        generation_cost_evolution.append(fitness_generation)
        best_individual_cost_evolution.append(generation[0].cost)
        for constraint in Constants.CONSTRAINTS:
            best_individual_constraints_evolution[constraint].append(generation[0].cost_constraints[constraint])
        return fitness_generation

    def find_solution(self, parent_selection_type="ROULETTE", use_random_individual=False):
        computed_generation = 0
        generated_individuals = self.generate_initial_population(computed_generation)
        computed_generation += 1
        generation = self.order_generation_by_cost(generated_individuals)
        best_individual_cost_evolution = []
        generation_cost_evolution = []
        best_individual_constraints_evolution = {}

        # region ADD INITIAL COSTS
        best_individual_cost_evolution.append(generation[0].cost)
        generation_cost_evolution.append(sum([individual.cost for individual in generation]))
        for constraint in Constants.CONSTRAINTS:
            best_individual_constraints_evolution[constraint] = []
            best_individual_constraints_evolution[constraint].append(generation[0].cost_constraints[constraint])
        # endregion

        if use_random_individual:
            generations_with_no_improvement = 0

        add_random_individual = False
        random_chromosome = None
        # REPEAT UNTIL CONDITION IS MET
        while computed_generation <= Constants.MAXIMUM_GENERATIONS:
            print("______________________________")
            # Calculate the old generation's cost to be able to compare if we have improved in
            # the next generation
            old_fitness = sum([individual.cost for individual in generation])
            # SELECT PARENTS
            parent_options = []
            if parent_selection_type == Constants.Parent_Selection_Type.ROULETTE:
                parent_options = self.choose_parents_roulette(generation, old_fitness)
            elif parent_selection_type == Constants.Parent_Selection_Type.TOURNAMENT:
                parent_options = self.choose_parents_tournament(generation)
            else:
                break

            if add_random_individual:
                parent_options.pop()
                parent_options.append(random_chromosome)
                add_random_individual = False

            # RECOMBINE PARENTS TO GENERATE OFFSPRINGS
            generated_individuals, parents = self.generate_offsprings(parent_options, computed_generation)
            # MUTATE
            self.mutate_offsprings(generated_individuals)
            # EVALUATE EACH CANDIDATE
            for individual in generated_individuals:
                individual.cost = self.fitness.calculate_fitness(individual)
            # SELECT NEXT GENERATION
            for parent in parents:
                if parent not in generated_individuals:
                    generated_individuals.append(parent)
            # Order the individuals of the generation by fitness cost
            new_generation = deepcopy(self.order_generation_by_cost(generated_individuals))
            print([individual.cost for individual in new_generation])
            generation = list(new_generation[i] for i in range(0, Constants.POPULATION_SIZE))
            fitness_generation = self.get_costs_generation(generation,
                                                           best_individual_cost_evolution,
                                                           best_individual_constraints_evolution,
                                                           generation_cost_evolution)
            print(
                f"Best individual: {generation[0].cost} generation: {generation[0].generation} individual: {generation[0].idx} "
                f"constraints: {generation[0].cost_constraints}\n"
                f"Fitness generation: {fitness_generation}")
            self.improvement = (old_fitness - fitness_generation) / old_fitness

            if use_random_individual:
                if self.improvement == 0:
                    generations_with_no_improvement += 1

                if generations_with_no_improvement > 2:
                    random_chromosome = Chromosome(deepcopy(self.courses),
                                                   deepcopy(self.classes),
                                                   deepcopy(self.teachers),
                                                   computed_generation,
                                                   -1)
                    random_chromosome.generate_initial_individual()
                    random_chromosome.cost = self.fitness.calculate_fitness(random_chromosome)
                    generations_with_no_improvement = 0
                    add_random_individual = True
            print(f"Improvement: {self.improvement}\n")
            computed_generation += 1
        # RETURN CHROMOSOME WITH LEAST COST
        return generation[
                   0], best_individual_cost_evolution, best_individual_constraints_evolution, generation_cost_evolution
