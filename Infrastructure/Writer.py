import numpy as np
import xlwt
from datetime import datetime

import Constants


class Writer:

    def write_timetable(self, solution):
        style0 = xlwt.easyxf('font: name Constantia', num_format_str='#,##0.00')
        wb = xlwt.Workbook()
        now = datetime.now()
        ws = wb.add_sheet(f'Horario{now.strftime("%d_%m_%Y-%H_%M_%S")}')

        for column in solution.columns:
            for idx in solution.index:
                lesson = solution[column][idx]
                lesson_string = ""
                if lesson != 0:
                    class_ = lesson.class_
                    teacher = lesson.assigned_teacher
                    day = lesson.get_weekday()
                    hour = lesson.get_hour()
                    lesson_string = lesson_string + f"{day} {hour} {class_} with {teacher}\n"
                ws.write(column, Constants.COURSES.index(idx), lesson_string, style0)
        wb.save('resultados_horarios.xls')
