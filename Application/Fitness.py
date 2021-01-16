# Fitness functions for the chormosome evaluation
import Constants
from Application.Chromosome import Chromosome
import numpy as np


class Fitness:

    def calculate_fitness(self, individual: Chromosome):
        return (self.hard_constraint_1(individual) +
                self.hard_constraint_3(individual) +
                self.hard_constraint_4(individual) +
                self.hard_constraint_6(individual) +
                self.hard_constraint_7(individual) +
                ## SOFT CONSTRAINTS
                self.soft_constraint_2(individual) +
                self.soft_constraint_3(individual) +
                self.soft_constraint_5(individual) +
                self.soft_constraint_6(individual) +
                self.soft_constraint_8(individual))

    # region HARD CONSTRAINTS (BORRAR)
    def hard_constraint_1(self, individual: Chromosome):
        """
        H1: Una asignatura sólo la puede impartir el profesor asignado.
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
                    teacher_name = individual.timetable[t][course].assigned_teacher
                    class_ = individual.timetable[t][course].class_
                    # print(f"Assigned teacher: {teacher_name} Possible teachers: {[teacher for teacher in individual.classes[class_].list_teachers]}")
                    # Buscamos si en las asignaciones, coincide profesor y asignatura
                    # que toca en ese slot horario
                    if teacher_name not in individual.classes[class_].list_teachers:
                        n_penalties = n_penalties + 1
        cost = int(n_penalties * Constants.HCW * (Constants.BASE ** 5))
        #print(f"H1 cost: {cost}")
        return cost

    def hard_constraint_3(self, individual: Chromosome):
        """
        H3: Un profesor no puede impartir más de una asignatura a la misma hora.
        :param individual:
        :return:
        """
        n_penalties = 0
        t_slots = np.shape(individual.timetable)[1]
        # Recorrido del cromosoma para encontrar posibles discrepancias entre profesor
        # asignado a asignatura y asignatura con profesor diferente
        for t in range(t_slots):
            teachers = []
            for course in Constants.COURSES:
                lesson = individual.timetable[t][course]
                if lesson != 0:
                    teachers.append(individual.timetable[t][course].assigned_teacher)
                    teachers_unique = list(set(teachers))
                    if len(teachers) != len(teachers_unique):
                        diff = len(teachers) - len(teachers_unique)
                        n_penalties = n_penalties + (diff * Constants.HCW * (Constants.BASE ** diff))
        #print(f"H3 cost: {int(n_penalties)}")
        return int(n_penalties)

    def hard_constraint_4(self, individual: Chromosome):
        """
        H4: No se debe superar la duración semanal de cada asignatura.
        :param individual:
        :return:
        """
        penalty_hours = 0
        # Recorrido del cromosoma para encontrar posibles discrepancias entre horas
        # de la asignatura y el máximo para cada curso
        assigned_classes = {}
        for course in individual.courses:
            # print(f"\n{course}")
            course_classes_week = individual.timetable.loc[course]
            for course_class in course_classes_week:
                lesson = course_class
                if lesson != 0:
                    if lesson.class_ in assigned_classes:
                        assigned_classes[lesson.class_] = assigned_classes[lesson.class_] + 1
                    else:
                        assigned_classes[lesson.class_] = 1

            for lesson in assigned_classes:
                class_hours_assigned = assigned_classes[lesson]
                class_maximum_hours_week = individual.classes[lesson].hours_per_week
                # print(f"{lesson} Assigned: {class_hours_assigned} Max: {class_maximum_hours_week}")

                diff_hours = np.abs(class_hours_assigned - class_maximum_hours_week)
                penalty_hours = penalty_hours + (diff_hours * Constants.HCW * (Constants.BASE ** diff_hours))
        #print(f"H4 cost: {int(penalty_hours)}")
        return int(penalty_hours)

    def hard_constraint_6(self, individual: Chromosome):
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
                    teacher_name = individual.timetable[t][course].assigned_teacher
                    teacher_availability = individual.teachers[teacher_name].availability[t]
                    if teacher_availability < -1:
                        # print(f"Teacher: {teacher_name}")
                        n_penalties = n_penalties + np.abs(teacher_availability)
        cost = int(n_penalties * Constants.HCW * (Constants.BASE ** n_penalties))
        #print(f"H6 cost: {cost}")
        return cost

    def hard_constraint_7(self, individual: Chromosome):
        """
        H7: Un grupo de alumnos sólo puede realizar las asignaturas que tiene asignadas
        :param individual:
        :return:
        """
        penalty_classes_not_assigned = 0
        penalty_not_in_course = 0

        for course in individual.courses:
            # Coger las clases asignadas para este curso
            assigned_classes = {}

            course_classes_week = individual.timetable.loc[course]
            for course_class in course_classes_week:
                lesson = course_class
                if lesson != 0:
                    if lesson.class_ in assigned_classes:
                        assigned_classes[lesson.class_] = assigned_classes[lesson.class_] + 1
                    else:
                        assigned_classes[lesson.class_] = 1

            classes_of_course = [class_.class_name for class_ in individual.courses[course].list_classes]
            # Comprobar que todas las asignaturas del curso se han asignado
            # print(f"{course} classes: {classes_of_course}")
            # print(f"Assigned classes: {assigned_classes}")
            list_classes_not_assigned = []

            classes_course = individual.courses[course].list_classes
            for class_course in classes_course:
                if class_course.class_name not in assigned_classes:
                    list_classes_not_assigned.append(class_course.class_name)
                    penalty_classes_not_assigned = penalty_classes_not_assigned + 1
            # print(f"{course} classes not assigned: {list_classes_not_assigned}")

            # Comprobar si hay asignaturas que no son del curso

            list_classes_not_in_course = []
            for class_ in assigned_classes:
                if class_ not in classes_of_course:
                    if class_ not in list_classes_not_in_course:
                        list_classes_not_in_course.append(class_)
                    penalty_not_in_course = penalty_not_in_course + 1
            # print(f"classes not in {course}: {list_classes_not_in_course}\n")
        cost_classes = penalty_not_in_course + penalty_classes_not_assigned
        cost = int(cost_classes * Constants.HCW * (Constants.BASE ** cost_classes))
        #print(f"H7 cost: {cost}")
        return cost

    '''
    Restricciones HARD ya implícitas:
        - H2: Un grupo de alumnos no puede tener más de una asignatura a la misma hora.
        - H5: Una asignatura sólo se puede realizar dentro del horario lectivo establecido.
        - H8: Un grupo de alumnos no puede superar el total de horas semanales 
            establecidas para las clases. Al haber solo 35 slots, ya viene implícito
    '''

    # endregion

    # region SOFT CONSTRAIINTS
    def soft_constraint_2(self, individual: Chromosome):
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
        #print(f"S2 cost: {cost}")
        return cost

    def soft_constraint_3(self, individual: Chromosome):
        """
        S3: Una asignatura no se debe impartir en días consecutivos.
        :param individual:
        :return:
        """
        n_penalties = 0
        # We look at 2 days at a time (lunes martes, martes miércoles, miércoles jueves, jueves viernes)
        for course in individual.courses:
            # print(f"{course}")
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
                # print(classes)
                # print("____")
        cost = int(n_penalties * Constants.SCW)
        #print(f"S3 cost: {cost}")
        return cost

    '''
        def soft_constraint_4(self, individual: Chromosome):
        """
        S4: Un grupo de clase no debe tener al mismo profesor en asignaturas diferentes en el mismo día.
        :param individual:
        :return:
        """
        n_penalties = 0
        for course in individual.courses:
            # print(f"{course}")
            for day in range(1, Constants.DAYS_PER_WEEK + 1):
                teachers = []
                start_idx = (day - 1) * 7
                for day_tp in range(start_idx, start_idx + Constants.HOURS_PER_DAY):
                    #print(day_tp)

                # print("____")
        print(f"S4 cost: {n_penalties}")
        return n_penalties
    '''


    def soft_constraint_5(self, individual: Chromosome):
        """
        S5: Las “horas sueltas“ de un grupo de alumnos se deben poner al final del día.
        :param individual:
        :return:
        """
        n_penalties = 0
        for course in individual.courses:
            # print(f"{course}")
            lessons = [lesson for lesson in individual.timetable.loc[course]]
            empty_lessons_idx = [i for i, x in enumerate(lessons) if x == 0]
            for day in range(1, Constants.DAYS_PER_WEEK + 1):
                first_period = (day - 1) * 7
                last_period = (first_period + Constants.HOURS_PER_DAY) - 1
                # print(f"First period: {first_period} Last period {last_period} First permitted empty period: {last_period - 1}")
                misassigned_empty_periods = sum(map(lambda x: first_period <= x < last_period - 1, empty_lessons_idx))
                # print(number_empty_periods)
                n_penalties = n_penalties + (misassigned_empty_periods * Constants.SCW)
                # print("____")
            # print(f"Empty lessons idx: {empty_lessons_idx}")
            # print("____")
        #print(f"S5 cost: {int(n_penalties)}")
        return int(n_penalties)

    def soft_constraint_6(self, individual: Chromosome):
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
            # print(f"Teacher {individual.teachers[teacher].name} Availability: {availability}/{hours_per_week} Max free periods: {max_free_periods}")
            if availability > max_free_periods:
                n_penalties = n_penalties + 1
        #print(n_penalties)

        cost = int(n_penalties * Constants.SCW)
        #print(f"S6 cost: {cost}")
        return cost

    '''
        def soft_constraint_7(self, individual: Chromosome):
        """
        S7: El total de “horas sueltas“ se deben distribuir uniformemente entre todos los profesores.
        :param individual:
        :return:
        """
        n_penalties = 0
        percentage_free_time = 25

        total_free_periods_week = 0

        teachers_free_hours = {}

        # Calculamos total de horas libres de todos los profes
        for teacher in individual.teachers:
            availability = list(individual.teachers[teacher].availability).count(0)
            # print(f"Teacher: {teacher} free hours: {availability}")
            teachers_free_hours[teacher] = availability
            total_free_periods_week = total_free_periods_week + availability

        #print(total_free_periods_week)

        for teacher in teachers_free_hours:
            free_hours = teachers_free_hours[teacher]
            hours_per_week = individual.teachers[teacher].hours_per_week
            max_free_periods = np.round((hours_per_week * percentage_free_time) / 100)
            #print(
            #    f"Teacher {individual.teachers[teacher].name} Free hours/work hours: {free_hours}/{hours_per_week} Max free periods: {max_free_periods}")
        #print("________")

        return n_penalties
    '''


    def soft_constraint_8(self, individual: Chromosome):
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
                        # print(f"Teacher: {teacher} Free periods in day: {free_periods_in_day}"
                        #      f" Max free periods per day: {free_hours_per_day}")
                        n_penalties = n_penalties + 1
            # print("------")

        cost = int(n_penalties * Constants.SCW)
        #print(f"S8 cost: {cost}")
        return cost
    # endregion
