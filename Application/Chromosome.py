import sys

import numpy as np
import pandas as pd
import random

import Constants
from Domain.Class import Lesson


class Chromosome:

    def __init__(self, courses, teachers, classes):
        self.courses = courses
        self.teachers = teachers
        self.classes = classes
        self.timetable = pd.DataFrame(
            np.zeros((
                len(courses),
                Constants.HOURS_PER_DAY * Constants.DAYS_PER_WEEK), dtype=int),
            index=courses.keys())
        self.cost = sys.maxsize

    def generate(self):
        for course in self.courses:
            total_slots = len(self.timetable.columns)
            total_slots_to_complete = random.randint(0, len(self.timetable.columns))
            slots_to_complete_idx = random.sample(range(total_slots), total_slots_to_complete)
            for time_slot in slots_to_complete_idx:
                teacher_name, _ = random.choice(list(self.teachers.items()))
                teacher = self.teachers[teacher_name]
                # If we assign the teacher to an unavailable time_slot
                # show it
                if teacher.availability[time_slot] == -1:
                    teacher.availability[time_slot] = -2
                else:
                    teacher.availability[time_slot] = 1
                class_, _ = random.choice(list(self.classes.items()))
                lesson = Lesson(teacher_name, class_, time_slot)
                self.timetable._set_value(course, time_slot, lesson)
        return self
