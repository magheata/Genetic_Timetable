# -*- coding: utf-8 -*-
# @Time    : 19/01/2021 21:49
# @Author  : Miruna Andreea Gheata, Pablo González Maya, Mateu Jover Mulet
# @Email   : miruna.gheata1@estudiant.uib.cat
# @File    : Class.py
# @Software: PyCharm

import Constants
from Domain.Course import Course
from Domain.Teacher import Teacher


class Class:
    def __init__(self, class_name: str, teacher: Teacher):
        self.class_name = class_name
        self.teacher = teacher
        self.course = []
        self.hours_per_week = None

    def set_class_course(self, course: Course):
        self.course.append(course)

    def set_hours_per_week(self, hours_per_week: int):
        self.hours_per_week = hours_per_week


class Lesson:
    def __init__(self, assigned_teacher: str, class_: str, time_slot: int):
        self.assigned_teacher = assigned_teacher
        self.class_ = class_
        self.time_slot = time_slot

    def get_weekday(self):
        """

        :return:
        """
        return Constants.WEEK_DAYS[int(self.time_slot / Constants.HOURS_PER_DAY)]

    def get_hour(self):
        """

        :return:
        """
        return Constants.HOUR_START_DAY + self.time_slot % Constants.HOURS_PER_DAY