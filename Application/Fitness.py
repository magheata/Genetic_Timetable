# -*- coding: utf-8 -*-
# @Time    : 19/01/2021 21:49
# @Author  : Miruna Andreea Gheata, Pablo González Maya, Mateu Jover Mulet
# @Email   : miruna.gheata1@estudiant.uib.cat
# @File    : Fitness.py
# @Software: PyCharm

import Constants
from Application.Chromosome import Chromosome
import numpy as np


class Fitness:

    def calculate_fitness(self, individual: Chromosome):
        """
        Calculate the total cost function of a chromosome. This cost determines how far the timetable is from being a
        solution. The goal is to minimize this cost function.
        :param individual:
        :return:
        """
        return (self.hard_constraint_1(individual) + self.hard_constraint_5(individual) +
                self.soft_constraint_1(individual) + self.soft_constraint_2(individual) +
                self.soft_constraint_3(individual) + self.soft_constraint_4(individual) +
                self.soft_constraint_5(individual)
                )

    # region HARD CONSTRAINTS

    @staticmethod
    def hard_constraint_1(individual: Chromosome):
        """
        H1: A teacher can't teach more than one lesson at the same time.
        :param individual: chromosome to evaluate.
        :return:
        """
        # Used to count the number of times the individual has more than one teacher assigned to one time period.
        n_penalties = 0
        # Get the total number of time slots
        t_slots = np.shape(individual.timetable)[1]
        # Check the timetable vertically. For each time slot, check if the teacher is assigned to teach in more than
        # one course
        for t in range(0, t_slots - 1):
            # List of assigned teacher in this time slot
            teachers = []
            # Check all courses
            for course in Constants.COURSES:
                # Get the lesson to access the teacher giving it
                lesson = individual.timetable[t][course]
                # If it is a lesson and not an empty period
                if lesson != 0:
                    # Add teacher to the list of assigned teacher
                    teachers.append(individual.timetable[t][course].assigned_teacher)
                    # Get the unique set of teachers assigned
                    teachers_unique = list(set(teachers))
                    # If lists are not equal, it mean that at least one teacher has been assigned more than once in this
                    # time slot
                    if len(teachers) != len(teachers_unique):
                        # Get the total number of teachers that have been assigned more than once
                        diff = len(teachers) - len(teachers_unique)
                        n_penalties = n_penalties + diff
        # Add the cost for this constraint to the individual
        individual.cost_constraints["H1"] = int(n_penalties * Constants.HCW)
        return int(n_penalties * Constants.HCW)

    @staticmethod
    def hard_constraint_5(individual: Chromosome):
        """
        H5: Teacher can only give lessons during their available hours.
        :param individual: chromosome to evaluate.
        :return:
        """
        # Used to count the number of times the individual has a timetable where a teacher gives a class outside the
        # availability
        n_penalties = 0
        t_slots = np.shape(individual.timetable)[1]
        # Check all time slots in a week
        for t in range(t_slots):
            # Check each course
            for course in Constants.COURSES:
                # Get the lesson taught at this time period in this course
                lesson = individual.timetable[t][course]
                # If not an empty period
                if lesson != 0:
                    # Get teacher and check availability
                    teacher_name = lesson.assigned_teacher
                    teacher_availability = individual.teachers[teacher_name].availability[t]
                    # If availability is less that -1 it means that the teacher was assigned during an unavailable time
                    # period
                    if teacher_availability < -1:
                        n_penalties = n_penalties + np.abs(teacher_availability)
        # Compute the cost and add to the individual's constraint cost
        cost = int(n_penalties * Constants.HCW)
        individual.cost_constraints["H5"] = cost
        return cost
    # endregion

    # region SOFT CONSTRAIINTS
    @staticmethod
    def soft_constraint_1(individual: Chromosome):
        """
        S1: A course should have few empty periods over the course of a day.
        :param individual: chromosome to evaluate.
        :return:
        """
        # Used to count the number of empty periods over the course of the day the timetable has for all courses
        n_penalties = 0
        t_slots = np.shape(individual.timetable)[1]
        # For all courses
        for course in Constants.COURSES:
            # Check time slot
            for t in range(t_slots):
                lesson = individual.timetable[t][course]
                # If it's an empty period, count it
                if lesson == 0:
                    n_penalties = n_penalties + 1
        # Compute the cost
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S1"] = cost
        return cost

    @staticmethod
    def soft_constraint_2(individual: Chromosome):
        """
        S3: A class should not be taught in consecutive days. This will be evaluated by checking each time a pair of days
        (Monday and Tuesday, Tuesday and Wednesday, and so forth). Therefore, this constraint will be unsatisfied if
        - The class is taught in the same day.
        - The class is taught in consecutive days.
        :param individual: chromosome to evaluate.
        :return:
        """
        # Used to count the number of classes taught in consecutive days
        n_penalties = 0
        # For all courses
        for course in individual.courses:
            # For each day of the week
            for day in range(1, Constants.DAYS_PER_WEEK):
                # Used to know the classes that are being taught in these time periods
                classes = []
                # First idx of first day
                start_idx = (day - 1) * 7
                # Last idx of second day
                end_idx = start_idx + (2 * Constants.HOURS_PER_DAY)
                # Check time periods in the first and second day
                for day_tp in range(start_idx, end_idx):
                    lesson = individual.timetable[day_tp][course]
                    if lesson != 0:
                        # If the class is already taught, count it as a penalty
                        if lesson.class_ in classes:
                            n_penalties = n_penalties + 1
                        # If not, append this class to the list
                        else:
                            classes.append(lesson.class_)
        # Compute the total cost and append it to the individual's constraints cost
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S2"] = cost
        return cost

    @staticmethod
    def soft_constraint_3(individual: Chromosome):
        """
        S3: The empty periods of a curse should be at the end of the day.
        :param individual: chromosome to evaluate.
        :return:
        """
        # Used to count the number of empty periods that are not at the end of the day
        n_penalties = 0
        # Check each course
        for course in individual.courses:
            # Get the total lessons taught over the course of a week
            lessons = [lesson for lesson in individual.timetable.loc[course]]
            # Get the indexes of the lessons that are empty periods
            empty_lessons_idx = [i for i, x in enumerate(lessons) if x == 0]
            # For each weekday, calculate the start and the end of the school periods
            for day in range(1, Constants.DAYS_PER_WEEK + 1):
                # First hour
                first_period = (day - 1) * 7
                # Last hour
                last_period = (first_period + Constants.HOURS_PER_DAY) - 1
                # Count the number of empty periods that are not at the end of the school day
                misassigned_empty_periods = sum(map(lambda x: first_period <= x < last_period - 1, empty_lessons_idx))
                # Add the total numbers of empty periods that are over the course of the day
                n_penalties = n_penalties + misassigned_empty_periods
        # Calculate the total cost and add it to the individual's constraints cost
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S3"] = cost
        return cost

    @staticmethod
    def soft_constraint_4(individual: Chromosome):
        """
        S4: Teachers should have few empty periods over the course of a school day.
        :param individual: chromosome to evaluate.
        :return:
        """
        # Used to count the number of teachers that have more empty periods that permitted over the course of a day
        n_penalties = 0
        # Percentage of empty periods that a teacher can have
        percentage_free_time = 25

        # Check all teachers
        for teacher in individual.teachers:
            # Get teacher's empty periods from the availability
            availability = list(individual.teachers[teacher].availability).count(0)
            # Compute the total number of empty periods that this teacher can have
            hours_per_week = individual.teachers[teacher].hours_per_week
            max_free_periods = np.round((hours_per_week * percentage_free_time) / 100)
            # If teacher has more empty lessons than allowed, count it as a penalty
            if availability > max_free_periods:
                n_penalties = n_penalties + 1
        # Calculate the total cost and add it to the individual's constraints cost
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S4"] = cost
        return cost

    @staticmethod
    def soft_constraint_5(individual: Chromosome):
        """
        S5: The total number of free periods should be distributed over the days the teacher is available at school.
        This means that if a teacher is at school 5 days and has 5 empty periods, there should be an empty period per
        day.
        :param individual: chromosome to evaluate.
        :return:
        """
        # Used to count the number of days that have more empty periods than permitted
        n_penalties = 0
        # Check all teachers
        for teacher in individual.teachers:
            # Get teacher's availability
            availability_teacher = list(individual.teachers[teacher].availability)
            # Get the number of free periods this teacher has
            free_hours = availability_teacher.count(0)
            # Get number of hours teacher is at school
            count_available_time_slots = sum(map(lambda x: x >= 0, availability_teacher))
            # Get number of days teacher is at school
            available_days = np.round(count_available_time_slots / Constants.HOURS_PER_DAY)
            # Compute total free periods per day this teacher can have
            free_hours_per_day = int(np.round(free_hours / available_days))
            # Now, check each week day if this maximum is satisfied
            for day in range(1, Constants.DAYS_PER_WEEK + 1):
                # Get first time period of day
                first_period = (day - 1) * 7
                # Get last time period of day
                last_period = first_period + Constants.HOURS_PER_DAY
                # Counter of free periods in this day
                free_periods_in_day = 0
                # For each time slot in this day
                for time_period in range(first_period, last_period):
                    # If teacher has free lesson, count it
                    if availability_teacher[time_period] == 0:
                        free_periods_in_day = free_periods_in_day + 1
                    # If teacher has surpassed maximum free periods, count it as a penalty
                    if free_periods_in_day > free_hours_per_day:
                        n_penalties = n_penalties + 1
        # Calculate the total cost and add it to the individual's constraints cost
        cost = int(n_penalties * Constants.SCW)
        individual.cost_constraints["S5"] = cost
        return cost
    # endregion
