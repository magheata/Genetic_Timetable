from Infrastructure.Loader import Loader
import pprint


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    loader = Loader()
    week_days, hours_per_day, start_time, end_time = loader.load_timetable_info()
    teachers = loader.load_teachers(week_days, hours_per_day)
    classes = loader.load_classes(teachers)
    courses = loader.load_courses(classes)
    print(pprint.pformat(courses['2BATX']))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
