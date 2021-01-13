import Constants
from Application.GeneticAlgorithm import GeneticAlgorithm
from Application.TimeTable import TimeTable
from Infrastructure.Loader import Loader


# Press the green button in the gutter to run the script.
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
    solution = geneticAlgorithm.find_solution()
    #print(solution)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
