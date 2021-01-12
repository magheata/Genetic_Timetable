import Constants
from Domain.Course import Course
from Domain.Teacher import Teacher


class Class:
    def __init__(self, class_name: str, list_teachers: dict):
        self.class_name = class_name
        self.list_teachers = list_teachers
        self.course = []
        self.hours_per_week = None

    def __repr__(self):
        return f"Class: {self.class_name}\n" \
               f"   Teachers: {self.list_teachers}\n" \
               f"   Course: {self.course}\n" \
               f"   Hours/Week: {self.hours_per_week}\n"

    def set_class_course(self, course: Course):
        self.course.append(course)

    def set_hours_per_week(self, hours_per_week: int):
        self.hours_per_week = hours_per_week


class Lesson:
    def __init__(self, assigned_teacher: Teacher, class_: Class, time_slot: int):
        self.assigned_teacher = assigned_teacher
        self.class_ = class_
        self.time_slot = time_slot

    def get_weekday(self):
        return Constants.WEEK_DAYS[int(self.time_slot / Constants.HOURS_PER_DAY)]

    def get_hour(self):
        return Constants.HOUR_START_DAY + self.time_slot % Constants.HOURS_PER_DAY

    def __repr__(self):
        return f"{self.class_.class_name}-{self.assigned_teacher.name}"
        #return f"   Assigned Teacher: {self.assigned_teacher}\n" \
        #       f"   Class: {self.class_}\n" \
        #       f"   Time slot: {self.time_slot}\n" \
        #       f"   Day: {Constants.WEEK_DAYS[int(self.time_slot / Constants.HOURS_PER_DAY)]}\n" \
        #       f"   Hour: { Constants.HOUR_START_DAY + self.time_slot % Constants.HOURS_PER_DAY}"
