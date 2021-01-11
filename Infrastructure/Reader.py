import pandas as pd


class Reader:

    @staticmethod
    def read_excel_sheet(excel_name, sheet_name):
        data = pd.read_excel(open(excel_name, 'rb'),
                             sheet_name=sheet_name)
        print(data)
