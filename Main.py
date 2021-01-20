import Constants
from Application.GeneticAlgorithm import GeneticAlgorithm
from Infrastructure.Loader import Loader
from datetime import datetime

from Infrastructure.Writer import Writer
from Infrastructure.Graphs import Graphs

if __name__ == '__main__':
    # Create Loader element to load the data from the Excel file
    loader = Loader()
    # Load timetable information (total days with classes,
    # hours per day, first hour of class day, las hour of
    # class day)
    courses, class_days, hours_per_day, start_time, end_time = loader.load_timetable_info()
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
    # Load teacher information (name, availability during the
    # week)
    teachers = loader.load_teachers(class_days, hours_per_day)
    # Load classes (name, list of teachers teach this class)
    classes = loader.load_classes(teachers)
    # Load courses (name, list of classes/course, hours per week);
    # the time information of the classes is also loaded here
    # (hours per class in the given course)
    courses = loader.load_courses(classes)

    geneticAlgorithm = GeneticAlgorithm(courses, classes, teachers)
    solution, cost_evolution, constraints_evolution, generation_cost_evolution = geneticAlgorithm.find_solution()
    writer = Writer()
    now = datetime.now()

    writer.write_timetable(solution, now.strftime("%d_%m_%Y-%H_%M_%S"))
    writer.write_evolution(cost_evolution, constraints_evolution, generation_cost_evolution, now.strftime("%d_%m_%Y-%H_%M_%S"))
    
    # Graphs
    visualizer = Graphs("Roulette selection", cost_evolution, generation_cost_evolution, constraints_evolution)
    visualizer.best_ind_plot()
    visualizer.generation_cost_plot()
    visualizer.best_ind_constraints_plot()
