# Fitness functions for the chormosome evaluation
import Constants
from Application.Chromosome import Chromosome
import numpy as np


class Fitness:

    def calculate_fitness(self, individual: Chromosome):

        return (self.hard_constraint_1(individual) + self.hard_constraint_5(individual) +
                self.soft_constraint_1(individual) + self.soft_constraint_2(individual) +
                self.soft_constraint_3(individual) + self.soft_constraint_4(individual) +
                self.soft_constraint_5(individual)
                )

    # region HARD CONSTRAINTS

    @staticmethod
    def hard_constraint_1(individual: Chromosome):
        """
        H3: Un profesor no puede impartir más de una asignatura a la misma hora.
        :param individual:
        :return:
        """
        n_penalties = 0
        t_slots = np.shape(individual.timetable)[1]

        # Recorrido del cromosoma para encontrar posibles discrepancias entre profesor
        # asignado a asignatura y asignatura con profesor diferente
        for t in range(0, t_slots - 1):
            teachers = []
            for course in Constants.COURSES:
                lesson = individual.timetable[t][course]
                if lesson != 0:
                    teachers.append(individual.timetable[t][course].assigned_teacher)
                    teachers_unique = list(set(teachers))
                    if len(teachers) != len(teachers_unique):
                        diff = len(teachers) - len(teachers_unique)
                        n_penalties = n_penalties + diff
        individual.cost_constraints["H1"] = int(n_penalties * Constants.HCW)
        #print(f"H3 cost: {int(n_penalties * Constants.HCW)}")
        #if n_penalties > 0:
        #    return Constants.HCW
        return int(n_penalties * Constants.HCW)
        #return 0

    @staticmethod
    def hard_constraint_5(individual: Chromosome):
        """
        H6: Los profesores sólo pueden dar clase en sus disponibilidades horarias.
        :param individual:
        :return:
        """
        n_penalties = 0
        t_slots = np.shape(individual.timetable)[1]
        # Recorrido del cromosoma para encontrar posibles discrepancias entre profesor
        # asignado a asignatura y asignatura con profesor diferente
        for t in range(t_slots):
            for course in Constants.COURSES:
                lesson = individual.timetable[t][course]
                if lesson != 0:
                    teacher_name = lesson.assigned_teacher
                    teacher_availability = individual.teachers[teacher_name].availability[t]
                    if teacher_availability < -1:
                        n_penalties = n_penalties + np.abs(teacher_availability)
        cost = int(n_penalties * Constants.HCW)
        individual.cost_constraints["H5"] = cost
        # print(f"H6 cost: {cost}")
        return cost

    '''
    Restricciones HARD ya implícitas:
        - H1: 
        - H2: Un grupo de alumnos no puede tener más de una asignatura a la misma hora.
        - H4
        - H5: Una asignatura sólo se puede realizar dentro del horario lectivo establecido.
        - H7
        - H8: Un grupo de alumnos no puede superar el total de horas semanales 
            establecidas para las clases. Al haber solo 35 slots, ya viene implícito
    '''

    # endregion

    # region SOFT CONSTRAIINTS
    @staticmethod
    def soft_constraint_1(individual: Chromosome):
        """
        S2: Un grupo de alumnos debe tener pocas “horas sueltas“ entre las asignaturas.
        :param individual:
        :return:
        """
        n_penalties = 0
        t_slots = np.shape(individual.timetable)[1]
        # Recorrido del cromosoma para encontrar posibles discrepancias entre profesor
        # asignado a asignatura y asignatura con profesor diferente

        for course in Constants.COURSES:
            for t in range(t_slots):
                lesson = individual.timetable[t][course]
                if lesson == 0:
                    n_penalties = n_penalties + 1
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S1"] = cost
        return cost

        '''
            Añadir una HC que sea no tener una misma clase en más de una hora en un día.
        '''

    @staticmethod
    def soft_constraint_2(individual: Chromosome):
        """
        S3: Una asignatura no se debe impartir en días consecutivos.
        :param individual:
        :return:
        """
        n_penalties = 0
        # We look at 2 days at a time (lunes martes, martes miércoles, miércoles jueves, jueves viernes)
        for course in individual.courses:
            for day in range(1, Constants.DAYS_PER_WEEK):
                classes = []
                # First idx of first day
                start_idx = (day - 1) * 7
                # Last idx of second day
                end_idx = start_idx + (2 * Constants.HOURS_PER_DAY)
                for day_tp in range(start_idx, end_idx):
                    lesson = individual.timetable[day_tp][course]
                    if lesson != 0:
                        if lesson.class_ in classes:
                            n_penalties = n_penalties + 1
                        else:
                            classes.append(lesson.class_)
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S2"] = cost
        return cost

    @staticmethod
    def soft_constraint_3(individual: Chromosome):
        """
        S5: Las “horas sueltas“ de un grupo de alumnos se deben poner al final del día.
        :param individual:
        :return:
        """
        n_penalties = 0
        for course in individual.courses:
            lessons = [lesson for lesson in individual.timetable.loc[course]]
            empty_lessons_idx = [i for i, x in enumerate(lessons) if x == 0]
            for day in range(1, Constants.DAYS_PER_WEEK + 1):
                first_period = (day - 1) * 7
                last_period = (first_period + Constants.HOURS_PER_DAY) - 1
                misassigned_empty_periods = sum(map(lambda x: first_period <= x < last_period - 1, empty_lessons_idx))
                n_penalties = n_penalties + (misassigned_empty_periods * Constants.SCW)
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S3"] = cost
        return cost

    @staticmethod
    def soft_constraint_4(individual: Chromosome):
        """
        S6: Los profesores deben tener el mínimo número de “horas sueltas“ durante el día.
        :param individual:
        :return:
        """
        n_penalties = 0
        percentage_free_time = 25

        for teacher in individual.teachers:
            availability = list(individual.teachers[teacher].availability).count(0)
            hours_per_week = individual.teachers[teacher].hours_per_week
            max_free_periods = np.round((hours_per_week * percentage_free_time) / 100)
            if availability > max_free_periods:
                n_penalties = n_penalties + 1

        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S4"] = cost
        return cost

    @staticmethod
    def soft_constraint_5(individual: Chromosome):
        """
        S8: El total de “horas sueltas“ que tiene un profesor se deben distribuir
         uniformemente entre los días que está disponible.
        :param individual:
        :return:
        """
        n_penalties = 0

        # Calculamos total de horas libres de todos los profes
        for teacher in individual.teachers:
            availability_teacher = list(individual.teachers[teacher].availability)
            free_hours = availability_teacher.count(0)
            count_available_time_slots = sum(map(lambda x: x >= 0, availability_teacher))

            available_days = np.round(count_available_time_slots / Constants.HOURS_PER_DAY)

            free_hours_per_day = int(np.round(free_hours / available_days))

            for day in range(1, Constants.DAYS_PER_WEEK + 1):
                first_period = (day - 1) * 7
                last_period = first_period + Constants.HOURS_PER_DAY
                free_periods_in_day = 0
                for time_period in range(first_period, last_period):
                    if availability_teacher[time_period] == 0:
                        free_periods_in_day = free_periods_in_day + 1
                    if free_periods_in_day > free_hours_per_day:
                        n_penalties = n_penalties + 1
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S5"] = cost
        return cost
    # endregion
