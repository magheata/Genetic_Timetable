import pandas as pd

import Constants


class Reader:

    @staticmethod
    def read_excel_sheet(sheet_name):
        return pd.read_excel(open(Constants.FILE_EXCEL_DATA, 'rb'),
                             sheet_name=sheet_name)
