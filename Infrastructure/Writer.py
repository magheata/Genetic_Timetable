import numpy as np
import xlwt
from xlutils.copy import copy
from xlrd import open_workbook
import os.path

import Constants


class Writer:

    @staticmethod
    def write_timetable(solution, file_name):
        """

        :param solution:
        :return:
        """

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

        ws = wb.add_sheet(f'Horario_{file_name}')

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

    def write_evolution(self, cost_evolution, constraints_evolution, generation_cost_evolution, file_name):
        style0 = xlwt.easyxf('font: name Constantia', num_format_str='#,##0.00')
        wb = None
        if os.path.isfile(Constants.FILE_EXCEL_EVOLUTION):
            rb = open_workbook(Constants.FILE_EXCEL_EVOLUTION)
            wb = copy(rb)
        else:
            wb = xlwt.Workbook(Constants.FILE_EXCEL_EVOLUTION)

        ws = wb.add_sheet(f'Horario_{file_name}')

        row_aux = 0
        ws.write(row_aux, 0, "Best individual cost", style0)
        row_aux += 1
        for idx in range(0, len(cost_evolution)):
            ws.write(row_aux, 0, cost_evolution[idx], style0)
            row_aux += 1

        row_aux = 0
        ws.write(row_aux, 1, "Generation cost", style0)
        row_aux += 1
        for idx in range(0, len(generation_cost_evolution)):
            ws.write(row_aux, 1, generation_cost_evolution[idx], style0)
            row_aux += 1

        column = 2
        for constraint_values in constraints_evolution.values():
            row_aux = 0
            ws.write(row_aux, column, Constants.CONSTRAINTS[column - 2], style0)
            row_aux += 1
            for value in constraint_values:
                ws.write(row_aux, column, value, style0)
                row_aux += 1
            column += 1
        wb.save(Constants.FILE_EXCEL_EVOLUTION)
