import Constants
from Domain.Class import Class
from Domain.Course import Course
from Domain.Teacher import Teacher
from Infrastructure.Reader import Reader
import pandas as pd
from copy import deepcopy


class Loader:

    def __init__(self):
        self._reader = Reader()

    def load_sheet(self, sheet_name: str):
        return self._reader.read_excel_sheet(sheet_name)

    def load_timetable_info(self):
        info_sheet = self._reader.read_excel_sheet(Constants.SHEET_INFO)
        week_days = None
        hours_per_day = None
        start_time = None
        end_time = None
        courses = None
        for index, row in info_sheet.iterrows():
            if not pd.isna(row['Días']):
                week_days = int(row['Días'])
                hours_per_day = int(row['Horas/día'])
                start_time = int(row['Hora inicio'])
                end_time = int(row['Hora fin'])
                courses = row['Cursos'].split(',')
                strip_list = [course.strip() for course in courses]
                courses = strip_list
        return courses, week_days, hours_per_day, start_time, end_time

    def load_teachers(self, week_days: list, hours_per_day: int):
        teacher_sheet = self._reader.read_excel_sheet(Constants.SHEET_TEACHER_INFO)
        teachers = {}
        for index, row in teacher_sheet.iterrows():
            if not pd.isna(row['Profesor']):
                teacher_name = row['Profesor'].strip()
                availability = {}
                teacher_availability = {}
                for weekday in Constants.WEEK_DAYS:
                    if row[weekday] != 'X':
                        teacher_availability[weekday] = 0
                    else:
                        teacher_availability[weekday] = -1
                total_hours_week = int(row['HORAS'])
                availability['weekdays'] = teacher_availability
                availability['class_days'] = week_days
                availability['hours_per_day'] = hours_per_day

                teachers[teacher_name] = Teacher(name=teacher_name,
                                                 availability=availability,
                                                 hours_per_week=total_hours_week)
        return teachers

    def load_courses(self, classes: dict):
        courses_sheet = self._reader.read_excel_sheet(Constants.SHEET_COURSE_HOURS_INFO)
        courses = {}
        for index, row in courses_sheet.iterrows():
            if not pd.isna(row['Curso']) and not (row['Curso'] in courses):
                course_name = row['Curso'].strip()
                class_name = row['Asignatura'].strip()
                class_hours_per_week = int(row['Total horas/clase semanales'])
                course_hours_week = int(row['Horas semanales curso'])
                class_ = deepcopy(classes[class_name])
                class_.set_class_course(course_name)
                class_.set_hours_per_week(class_hours_per_week)
                courses[course_name] = Course(course_name, course_hours_week)
                courses[course_name].list_classes[class_name] = class_
            elif row['Curso'] in courses:
                class_name = row['Asignatura'].strip()
                class_hours_per_week = int(row['Total horas/clase semanales'])
                class_ = deepcopy(classes[class_name])
                class_.set_class_course(row['Curso'].strip())
                class_.set_hours_per_week(class_hours_per_week)
                courses[row['Curso']].list_classes[class_name] = class_
        return courses

    def load_classes(self, teachers: dict):
        class_sheet = self._reader.read_excel_sheet(Constants.SHEET_CLASS_TEACHERS_INFO)
        classes = {}
        for index, row in class_sheet.iterrows():
            if not pd.isna(row['Asignatura']):
                class_name = row['Asignatura'].strip()
                if not pd.isna(row['Profesor 1']):
                    teacher = teachers[row['Profesor 1'].strip()]
                    classes[class_name] = Class(class_name=class_name,
                                                teacher=teacher)
        return classes
