import numpy as np
import xlwt
from xlutils.copy import copy
from xlrd import open_workbook
from datetime import datetime
import os.path

import Constants


class Writer:

    def write_timetable(self, solution):

        timetable = solution.timetable

        info_indivudual = f"Cost: {solution.cost} generation: {solution.generation} individual: {solution.idx} " \
                          f"constraints: {solution.cost_constraints}"

        style0 = xlwt.easyxf('font: name Constantia', num_format_str='#,##0.00')
        wb = None
        if os.path.isfile(Constants.FILE_EXCEL_RESULTS):
            rb = open_workbook(Constants.FILE_EXCEL_RESULTS)
            wb = copy(rb)
        else:
            wb = xlwt.Workbook(Constants.FILE_EXCEL_RESULTS)

        now = datetime.now()
        ws = wb.add_sheet(f'Horario{now.strftime("%d_%m_%Y-%H_%M_%S")}')

        for column in timetable.columns:
            for idx in timetable.index:
                lesson = timetable[column][idx]
                lesson_string = ""
                if lesson != 0:
                    class_ = lesson.class_
                    teacher = lesson.assigned_teacher
                    day = lesson.get_weekday()
                    hour = lesson.get_hour()
                    lesson_string = lesson_string + f"{day} {hour} {class_} with {teacher}\n"
                ws.write(column, Constants.COURSES.index(idx), lesson_string, style0)
        ws.write(Constants.HOURS_PER_DAY * Constants.DAYS_PER_WEEK + 1, 0, info_indivudual, style0)

        wb.save(Constants.FILE_EXCEL_RESULTS)
