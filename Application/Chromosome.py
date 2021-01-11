import numpy as np
import pandas as pd

from Domain.Class import Lesson


class Chromosome:

    def __init__(self, courses, teachers, total_time_slots):
        self.teachers = teachers
        self.timetable = pd.DataFrame(
            np.zeros((len(courses), total_time_slots), dtype=int),
            index=courses.keys())
        idx = 10
        self.timetable[idx]['1ESO'] = Lesson('test', 'test', idx)
        print(self.timetable[idx]['1ESO'])
