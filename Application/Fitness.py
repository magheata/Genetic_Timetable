# Fitness functions for the chormosome evaluation
import Constants
from Application.Chromosome import Chromosome
import numpy as np


class Fitness:

    def calculate_fitness(self, individual: Chromosome):
        return (self.hard_constraint_1(individual) + self.hard_constraint_3(individual) +
                self.hard_constraint_4(individual) + self.hard_constraint_6(individual) +
                self.hard_constraint_7(individual))

    @staticmethod
    def hard_constraint_1(individual: Chromosome):
        """
        H1: Una asignatura sólo la puede impartir el profesor asignado.
        """
        n_penalties = 0
        total_teachers_checked = 0
        t_slots = np.shape(individual.timetable)[1]
        # Recorrido del cromosoma para encontrar posibles discrepancias entre profesor
        # asignado a asignatura y asignatura con profesor diferente
        for t in range(t_slots):
            for course in Constants.COURSES:
                lesson = individual.timetable[t][course]
                if lesson != 0:
                    teacher_name = individual.timetable[t][course].assigned_teacher.name
                    class_ = individual.timetable[t][course].class_
                    # print(f"Assigned teacher: {teacher_name} Possible teachers: {[teacher.name for teacher in class_.list_teachers]}")
                    # Buscamos si en las asignaciones, coincide profesor y asignatura
                    # que toca en ese slot horario
                    if teacher_name not in class_.list_teachers:
                        n_penalties = n_penalties + 1
                    total_teachers_checked = total_teachers_checked + 1
        print(f"H1 cost: {n_penalties}")
        return n_penalties

    @staticmethod
    def hard_constraint_3(individual: Chromosome):
        """
        H3: Un profesor no puede impartir más de una asignatura a la misma hora.
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
                        n_penalties = n_penalties + (len(teachers) - len(teachers_unique))
        print(f"H3 cost: {n_penalties}")
        return n_penalties

    @staticmethod
    def hard_constraint_4(individual: Chromosome):
        """
        H4: No se debe superar la duración semanal de cada asignatura.
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
                    if lesson.class_.class_name in assigned_classes:
                        assigned_classes[lesson.class_.class_name] = assigned_classes[lesson.class_.class_name] + 1
                    else:
                        assigned_classes[lesson.class_.class_name] = 1

            for lesson in assigned_classes:
                class_hours_assigned = assigned_classes[lesson]
                class_maximum_hours_week = individual.classes[lesson].hours_per_week
                # print(f"{lesson} Assigned: {class_hours_assigned} Max: {class_maximum_hours_week}")
                penalty_hours = penalty_hours + np.abs(class_hours_assigned - class_maximum_hours_week)
        print(f"H4 cost: {penalty_hours}")
        return penalty_hours

    @staticmethod
    def hard_constraint_6(individual: Chromosome):
        """
        H6: Los profesores sólo pueden dar clase en sus disponibilidades horarias.
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
                    if individual.teachers[teacher_name.name].availability[t] == -2:
                        #print(f"Teacher: {teacher_name.name}")
                        n_penalties = n_penalties + 1
        print(f"H6 cost: {n_penalties}")
        return n_penalties

    @staticmethod
    def hard_constraint_7(individual: Chromosome):
        """
        H7: Un grupo de alumnos sólo puede realizar las asignaturas que tiene asignadas
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
                    if lesson.class_.class_name in assigned_classes:
                        assigned_classes[lesson.class_.class_name] = assigned_classes[lesson.class_.class_name] + 1
                    else:
                        assigned_classes[lesson.class_.class_name] = 1

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
        print(f"H7 cost: {penalty_not_in_course + penalty_classes_not_assigned}")
        return penalty_not_in_course + penalty_classes_not_assigned

    '''
    Restricciones HARD ya implícitas:
        - H2: Un grupo de alumnos no puede tener más de una asignatura a la misma hora.
        - H5: Una asignatura sólo se puede realizar dentro del horario lectivo establecido.
        - H8: Un grupo de alumnos no puede superar el total de horas semanales 
            establecidas para las clases. Al haber solo 35 slots, ya viene implícito
    '''
