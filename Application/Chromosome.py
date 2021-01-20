# -*- coding: utf-8 -*-
# @Time    : 19/01/2021 21:49
# @Author  : Miruna Andreea Gheata, Pablo González Maya, Mateu Jover Mulet
# @Email   : miruna.gheata1@estudiant.uib.cat
# @File    : Chromosome.py
# @Software: PyCharm

import sys

import numpy as np
import pandas as pd
import random

from copy import deepcopy

import Constants
import numpy as np
import pandas as pd
import random

from copy import deepcopy

import Constants
from Domain.Class import Lesson


class Chromosome:

    def __init__(self, courses: dict, classes: dict, teachers: dict, generation: int, idx: int):
        """
        Chromosome constructor. Contains the information of an individual of the problem.
        :param courses: courses that need to have their timetable computed.
        :param classes: classes available; each course has its own classes.
        :param teachers: teachers available to teach in each course. Each teacher has its own availability over the
        course of a school week.
        :param generation: the generation number to which this individual pertains to.
        :param idx: represents the order in which this individual was created (first individual has idx = 1,
        second individual has idx = 2, and so on)
        """
        self.generation = generation
        self.idx = idx
        # Initialize the cost to the maximum value. The goal is to minimize this cost. The smaller the cost,
        # the more correct this individual is.
        self.cost = sys.maxsize
        # Initially the timetable is empty
        self.timetable = None
        self.courses = courses
        self.classes = classes
        self.teachers = teachers
        # Dictionary that will contain the cost of each constraint
        self.cost_constraints = {}

    def compute_teacher_availability(self, teacher, time_slot):
        """
        Iterates over the timetable and updates the availability of each teacher in one week by checking each lesson
        that they teach. Given a lesson l in a time slot ts, the teacher can either:
        - Be available to teach l in ts.
        - Be unavailable to teach l because at time ts, the teacher is not at school.
        :param teacher: teacher that has to teach this lesson.
        :param time_slot: time period (day and hour) in which the lesson need to be taught.
        :return:
        """
        # If the value is negative, it means that the teacher is not available to teach
        if self.teachers[teacher].availability[time_slot] < 0:
            # We denote the teacher was assigned a lesson during an unavailable time. See that the value can be -2,
            # -3, -4... and so forth. The more the teacher is assigned lessons in this time period, the more negative
            # this value is.
            self.teachers[teacher].availability[time_slot] -= 1
        else:
            # The teacher is available. Go from availability 0 to 1 to show that the teacher is in a lesson.
            self.teachers[teacher].availability[time_slot] = 1

    def generate_initial_individual(self):
        """
        Initialize the timetable for this individual. The timetable is a DataFrame that has:
        - The courses as its rows.
        - The time slots as its columns.
        For each course, the classes that need to be taught are randomly assigned to a time slot until each class
        has reached its total hours per week.
        :return: the individual
        """
        # Initialize all cells of the timetable to 0. The cells that don't have a class assigned are considered to be
        # empty time periods (with value 0).
        self.timetable = pd.DataFrame(
            np.zeros((
                len(self.courses),
                Constants.HOURS_PER_DAY * Constants.DAYS_PER_WEEK), dtype=int),
            index=self.courses.keys())

        # Assign each course the classes that need to be taught in a week
        for course in self.courses:
            # Get the list of classes for this course
            list_classes = deepcopy(self.courses[course].list_classes)
            # Used to check when a class has reached its maximum weekly hours
            total_assigned_classes = {}
            # For each time slot of the week
            for time_slot in self.timetable.columns:
                # Used to control whether this class has been assigned its total hours in the week. If it is True,
                # select a new class to assign to this time slot.
                incorrect_class = True
                # Repeat while there has been no class assigned to this time slot and there are still classes to be
                # assigned
                while incorrect_class and list_classes:
                    # Select random class
                    class_idx = random.choice(list(list_classes.keys()))
                    class_ = self.courses[course].list_classes[class_idx]
                    # The class has already been assigned during a time slot
                    if class_.class_name in total_assigned_classes:
                        # If it has not reached the maximum number of hours per week, assign it to the current time slot
                        if total_assigned_classes[class_.class_name] < class_.hours_per_week:
                            self.compute_teacher_availability(class_.teacher.name, time_slot)
                            lesson = Lesson(class_.teacher.name, class_.class_name, time_slot)
                            self.timetable._set_value(course, time_slot, lesson)
                            total_assigned_classes[class_.class_name] += 1
                            # Show that the class was assigned so a new time slot needs to be filled next
                            incorrect_class = False
                        # The class has reached the maximum number of lessons
                        else:
                            # Delete class from the list to avoid selecting it again since its total hours have been
                            # assigned
                            del list_classes[class_.class_name]
                    # First time the class was selected, assign it to this time slot
                    else:
                        total_assigned_classes[class_.class_name] = 1
                        self.compute_teacher_availability(class_.teacher.name, time_slot)
                        lesson = Lesson(class_.teacher.name, class_.class_name, time_slot)
                        self.timetable._set_value(course, time_slot, lesson)
                        # Show that the class was assigned so a new time slot needs to be filled next
                        incorrect_class = False
        return self

    def calculate_teachers_availability(self):
        """
        Compute all teachers' availability by applying the function above.
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
        Set value of the timetable.
        :param timetable: value for this individual's timetable.
        :return:
        """
        self.timetable = timetable

