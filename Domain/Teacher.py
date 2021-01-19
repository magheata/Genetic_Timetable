# -*- coding: utf-8 -*-
# @Time    : 19/01/2021 21:49
# @Author  : Miruna Andreea Gheata, Pablo González Maya, Mateu Jover Mulet
# @Email   : miruna.gheata1@estudiant.uib.cat
# @File    : Teacher.py
# @Software: PyCharm

import numpy as np


class Teacher:
    def __init__(self, name: str, availability: dict, hours_per_week: int):
        self.name = name
        self.aux_availability = availability
        self.availability = np.zeros(self.aux_availability['class_days'] *
                                     self.aux_availability['hours_per_day'])
        availability_idx = 0
        for availability_class_day in self.aux_availability['weekdays']:
            for i in range(0, self.aux_availability['hours_per_day']):
                self.availability[availability_idx] = self.aux_availability['weekdays'][availability_class_day]
                availability_idx = availability_idx + 1
        self.hours_per_week = hours_per_week
