# -*- coding: utf-8 -*-
# @Time    : 19/01/2021 21:49
# @Author  : Miruna Andreea Gheata, Pablo González Maya, Mateu Jover Mulet
# @Email   : miruna.gheata1@estudiant.uib.cat
# @File    : Course.py
# @Software: PyCharm

class Course:

    def __init__(self, name: str, weekly_hours: int):
        self.name = name
        self.list_classes = {}
        self.weekly_hours = weekly_hours