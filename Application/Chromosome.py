import numpy as np
import pandas as pd

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
        self.cost = 10000000000000000

    def create(self):
        return self
