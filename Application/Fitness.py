# Fitness functions for the chormosome evaluation
from Application.Chromosome import Chromosome
from Domain.Class import Class
import numpy as np


YEARS = ['1ESO', '2ESO', '3ESO', '4ESO', '1BATX', '2BATX']
'''
H1: Una asignatura sólo la puede impartir el profesor asignado.
'''
def hard_constraint_1(individual : Chromosome, asignaciones : list):
    n_penalties = 0
    t_slots = np.shape(individual.timetable)[1]
    # Recorrido del cromosoma para encontrar posibles discrepancias entre profesor
    # asignado a asignatura y asignatura con profesor diferente
    for t in range(t_slots):
        for year in YEARS:
            teacher_name = individual.timetable[t][year].assigned_teacher
            class_ = individual.timetable[t][year].class_
            # Buscamos si en las asignaciones, coincide profesor y asignatura 
            # que toca en ese slot horario
            ok = False
            for i in range( len(asignaciones[class_].list_teachers) ):
                ok = ok | (asignaciones[class_].list_teachers[i].name == teacher_name)
            
            if not ok :
                n_penalties = n_penalties + 1
            
    return n_penalties



'''
H3: Un profesor no puede impartir más de una asignatura a la misma hora.
'''
def hard_constraint_3(individual : Chromosome):
    n_penalties = 0
    t_slots = np.shape(individual.timetable)[1]
    # Recorrido del cromosoma para encontrar posibles discrepancias entre profesor
    # asignado a asignatura y asignatura con profesor diferente
    for t in range(t_slots):
        teachers = []
        i = 0
        for year in YEARS:
            teachers[i] = individual.timetable[t][year].assigned_teacher
            i = i + 1
        teachers_unique = list( set(teachers) )
        if ( len(teachers) != len(teachers_unique)):
            n_penalties = n_penalties + (len(teachers) - len(teachers_unique))
    
    return n_penalties


'''
H4: No se debe superar la duración semanal de cada asignatura. 
'''

def hard_constraint_4(individual : Chromosome, asignaciones: list):
    n_penalties = 0
    t_slots = np.shape(individual.timetable)[1]
    # Recorrido del cromosoma para encontrar posibles discrepancias entre horas
    # de la asignatura y el máximo para cada curso
    
    
    return n_penalties


    
'''
H6: Los profesores sólo pueden dar clase en sus disponibilidades horarias.
'''

def hard_constraint_6(individual : Chromosome, claustro: dict):
    n_penalties = 0
    t_slots = np.shape(individual.timetable)[1]
    # Recorrido del cromosoma para encontrar posibles discrepancias entre profesor
    # asignado a asignatura y asignatura con profesor diferente
    for t in range(t_slots):
        for year in YEARS:
            teacher_name = individual.timetable[t][year].assigned_teacher
            if (claustro[teacher_name].availability[t] == -1):
                n_penalties = n_penalties + 1
            
    return n_penalties



'''
H7: Un grupo de alumnos sólo puede realizar las asignaturas que tiene asignadas
'''

def hard_constraint_7(individual : Chromosome, courses: dict):
    n_penalties = 0
    t_slots = np.shape(individual.timetable)[1]
    for year in YEARS:
        for t in range(t_slots):
            this_class = individual.timetable[t][year].class_
            plan_de_estudios = False
            for i in range( len(courses[year].list_classes) ):
                plan_de_estudios = plan_de_estudios | (courses[year].list_classes[i].class_name == this_class)
            
            if not plan_de_estudios:
                n_penalties = n_penalties + 1
                
    return n_penalties



'''
Restricciones HARD ya implícitas:
    - H2: Un grupo de alumnos no puede tener más de una asignatura a la misma hora.
    - H5: Una asignatura sólo se puede realizar dentro del horario lectivo establecido.
    - H8: Un grupo de alumnos no puede superar el total de horas semanales 
        establecidas para las clases. Al haber solo 35 slots, ya viene implícito
'''    