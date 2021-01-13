import Constants
import pandas as pd


class TimeTable:

    def __init__(self, timetable: pd.DataFrame, course: str):
        self.timetable = timetable
        self.course = course

    def __repr__(self):
        res = ""
        selected_course_timetable = self.timetable[self.course, :]
        for time_slot in self.timetable:
            lesson = selected_course_timetable[time_slot]
            if lesson != 0:
                class_ = lesson.class_
                teacher = lesson.assigned_teacher
                day = lesson.get_weekday()
                hour = lesson.get_hour()
                res = res + f"{day} {hour} {class_} with {teacher}\n"
        return res
