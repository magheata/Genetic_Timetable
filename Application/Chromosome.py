import sys

import numpy as np
import pandas as pd
import random

from copy import deepcopy

import Constants
from Domain.Class import Lesson


class Chromosome:

    def __init__(self, courses: dict, classes: dict, teachers: dict, generation: int, idx: int):
        self.generation = generation
        self.idx = idx
        self.cost = sys.maxsize
        self.timetable = None
        self.courses = courses
        self.classes = classes
        self.teachers = teachers
        self.cost_constraints = {}

    def compute_teacher_availability(self, teacher, time_slot):
        """

        :param teacher:
        :param time_slot:
        :return:
        """
        if self.teachers[teacher].availability[time_slot] < 0:
            self.teachers[teacher].availability[time_slot] -= 1
        else:
            self.teachers[teacher].availability[time_slot] = 1

    def generate_initial_individual(self):
        """

        :return:
        """
        self.timetable = pd.DataFrame(
            np.zeros((
                len(self.courses),
                Constants.HOURS_PER_DAY * Constants.DAYS_PER_WEEK), dtype=int),
            index=self.courses.keys())
        for course in self.courses:
            list_classes = deepcopy(self.courses[course].list_classes)
            total_assigned_classes = {}
            for time_slot in self.timetable.columns:
                incorrect_class = True
                while incorrect_class and list_classes:
                    class_idx = random.choice(list(list_classes.keys()))
                    class_ = self.courses[course].list_classes[class_idx]
                    if class_.class_name in total_assigned_classes:
                        if total_assigned_classes[class_.class_name] < class_.hours_per_week:
                            self.compute_teacher_availability(class_.teacher.name, time_slot)
                            lesson = Lesson(class_.teacher.name, class_.class_name, time_slot)
                            self.timetable._set_value(course, time_slot, lesson)
                            total_assigned_classes[class_.class_name] += 1
                            incorrect_class = False
                        else:
                            del list_classes[class_.class_name]
                    else:
                        total_assigned_classes[class_.class_name] = 1
                        self.compute_teacher_availability(class_.teacher.name, time_slot)
                        lesson = Lesson(class_.teacher.name, class_.class_name, time_slot)
                        self.timetable._set_value(course, time_slot, lesson)
                        incorrect_class = False
        return self

    def calculate_teachers_availability(self):
        """

        :return:
        """
        for course in self.courses:
            total_slots = len(self.timetable.columns)
            for time_slot in range(0, total_slots):
                lesson = self.timetable[time_slot][course]
                # Teacher not available in this assigned lesson
                if lesson != 0:
                    self.compute_teacher_availability(lesson.assigned_teacher, time_slot)

    def set_timetable(self, timetable):
        """

        :param timetable:
        :return:
        """
        self.timetable = timetable

