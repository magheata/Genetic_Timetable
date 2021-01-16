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

    def generate_initial_individual(self):
        self.timetable = pd.DataFrame(
            np.zeros((
                len(self.courses),
                Constants.HOURS_PER_DAY * Constants.DAYS_PER_WEEK), dtype=int),
            index=self.courses.keys())
        #print("Before", self.teachers["Andreu F."].availability)
        for course in self.courses:
            total_slots = len(self.timetable.columns)
            total_slots_to_complete = random.randint(0, len(self.timetable.columns))
            slots_to_complete_idx = random.sample(range(total_slots), total_slots_to_complete)
            for time_slot in slots_to_complete_idx:
                class_idx, _ = random.choice(list(self.classes.items()))
                class_ = self.classes[class_idx]
                teacher = class_.teacher
                if teacher.availability[time_slot] < 0:
                    teacher.availability[time_slot] -= 1
                else:
                    teacher.availability[time_slot] = 1
                lesson = Lesson(teacher.name, class_.class_name, time_slot)
                self.timetable._set_value(course, time_slot, lesson)
        #print("After", self.teachers["Andreu F."].availability, "\n")
        return self

    def calculate_teachers_availability(self):
        old_availability = deepcopy(self.teachers["Andreu F."].availability)
        print("Before", old_availability)
        for course in self.courses:
            total_slots = len(self.timetable.columns)
            for time_slot in range(0, total_slots):
                lesson = self.timetable[time_slot][course]
                if lesson != 0:
                    # Teacher not available in this assigned lesson
                    if self.teachers[lesson.assigned_teacher].availability[time_slot] < 0:
                        self.teachers[lesson.assigned_teacher].availability[time_slot] = -2
                    else:
                        # Teacher in class
                        self.teachers[lesson.assigned_teacher].availability[time_slot] = 1

        print("After", self.teachers["Andreu F."].availability, "\n")

    def set_timetable(self, timetable):
        self.timetable = timetable
