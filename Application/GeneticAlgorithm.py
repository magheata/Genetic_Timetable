import Constants
from Application.Chromosome import Chromosome
from Application.Fitness import Fitness


class GeneticAlgorithm:

    def __init__(self, courses: dict, classes: dict, teachers: dict):
        self.courses = courses
        self.classes = classes
        self.teachers = teachers
        self.population_size = 20
        self.mutation = 0.95
        self.percentage_of_improvement = 0.3
        self.improvement = 0
        self.fitness = Fitness()

    def find_solution(self):
        chromosomes = []

        # INITIALISE POPULATION WITH RANDOM CANDIDATE SOLUTION
        for i in range(0, self.population_size):
            chromosome = Chromosome(self.courses,
                                    self.teachers,
                                    self.classes)
            chromosomes.append(chromosome.generate())
        # EVALUATE EACH CANDIDATE

        for chromosome in chromosomes:
            chromosome.cost = self.fitness.calculate_fitness(chromosome)
            print(f"{chromosome.cost}\n")
        #REPEAT UNTIL CONDITION IS MET
        generations = 0
        while self.improvement < 0 and generations <= Constants.MAXIMUM_GENERATIONS:
            # SELECT PARENTS

            # RECOMBINATION

            # MUTATE

            # EVALUATE EACH CANDIDATE

            # SELECT NEXT GENERATION
            i = 0

        # RETURN CHROMOSOME WITH LEAST COST
        return chromosomes[0].timetable
