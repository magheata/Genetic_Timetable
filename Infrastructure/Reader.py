# -*- coding: utf-8 -*-
# @Time    : 19/01/2021 21:49
# @Author  : Miruna Andreea Gheata, Pablo González Maya, Mateu Jover Mulet
# @Email   : miruna.gheata1@estudiant.uib.cat
# @File    : Reader.py
# @Software: PyCharm

import pandas as pd

import Constants


class Reader:

    @staticmethod
    def read_excel_sheet(sheet_name: str):
        """

        :param sheet_name:
        :return:
        """
        return pd.read_excel(open(Constants.FILE_EXCEL_DATA, 'rb'),
                             sheet_name=sheet_name)
