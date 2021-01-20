# -*- coding: utf-8 -*-
# @Time    : 19/01/2021 21:49
# @Author  : Miruna Andreea Gheata, Pablo González Maya, Mateu Jover Mulet
# @Email   : miruna.gheata1@estudiant.uib.cat
# @File    : Main.py
# @Software: PyCharm

import Constants
from Application.GeneticAlgorithm import GeneticAlgorithm
from Infrastructure.Loader import Loader
from datetime import datetime

from Infrastructure.Writer import Writer

if __name__ == '__main__':
    # Create Loader element to load the data from the Excel files
    loader = Loader()
    # Load timetable information (total days with classes,
    # hours per day, first hour of class day, las hour of
    # class day)
    courses, class_days, hours_per_day, start_time, end_time = loader.load_timetable_info()
    print(f"Loading problem information from {Constants.FILE_EXCEL_DATA}/{Constants.SHEET_INFO}...")
    # Update project constants if necessary
    if Constants.COURSES != courses:
        Constants.COURSES = courses
    if Constants.HOURS_PER_DAY != hours_per_day:
        Constants.HOURS_PER_DAY = hours_per_day
    if Constants.DAYS_PER_WEEK != class_days:
        Constants.WEEK_DAYS = class_days
    if Constants.HOUR_START_DAY != start_time:
        Constants.HOUR_START_DAY = start_time
    if Constants.HOUR_END_DAY != end_time:
        Constants.HOUR_END_DAY = end_time
    # Load teacher information (name, availability during the week)
    teachers = loader.load_teachers(class_days, hours_per_day)
    print(f"Loading teachers from {Constants.FILE_EXCEL_DATA}/{Constants.SHEET_TEACHER_INFO}...")

    # Load classes (name, list of teachers teach this class)
    classes = loader.load_classes(teachers)
    print(f"Loading classes from {Constants.FILE_EXCEL_DATA}/{Constants.SHEET_CLASS_TEACHERS_INFO}...")

    # Load courses (name, list of classes/course, hours per week);
    # the time information of the classes is also loaded here (hours per class in the given course)
    courses = loader.load_courses(classes)
    print(f"Loading courses from {Constants.FILE_EXCEL_DATA}/{Constants.SHEET_COURSE_HOURS_INFO}...")

    print(f"Launching genetic algorithm computation to find a possible timetable solution...")
    print(f"Total generations to be computed: {Constants.MAXIMUM_GENERATIONS}\n")


    geneticAlgorithm = GeneticAlgorithm(courses, classes, teachers)
    # Define the parent selection algorithm
    parent_selection_type = Constants.Parent_Selection_Type.ROULETTE
    # Compute the timetable solution
    solution, cost_evolution, constraints_evolution, generation_cost_evolution = geneticAlgorithm.find_solution(parent_selection_type, True)
    # Initialize writer to save the results in an Excel file
    writer = Writer()
    now = datetime.now()
    # Write the resulting timetables (each column represents one specific course)
    writer.write_timetable(solution, f"{parent_selection_type.name}_{now.strftime('%d_%m_%Y-%H_%M_%S')}")
    # Write the cost evolution over the different iterations
    writer.write_evolution(cost_evolution, constraints_evolution, generation_cost_evolution, f"{parent_selection_type.name}_{now.strftime('%d_%m_%Y-%H_%M_%S')}")

    print(f"Done! Computed timetables can be found in file {Constants.FILE_EXCEL_RESULTS} and cost evolution in file {Constants.FILE_EXCEL_EVOLUTION}.")