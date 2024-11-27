import openpyxl
import xlrd
from xToolkit import xfile
from hctest_excel_to.excel_to import Excel
import pandas as pd


class ExcelReader:
    # def __init__(self, filePath, sheetName="Sheet1"):
    #     self.data = xlrd.open_workbook(filePath)
    #     self.table = self.data.sheet_by_name(sheetName)
    #
    #     # 获取第一行作为key值
    #     self.keys = self.table.row_values(0)
    #     # 获取总行数
    #     self.rowNum = self.table.nrows
    #     # 获取总列数
    #     self.colNum = self.table.ncols

    @staticmethod
    def read_data(file_path):
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)
        return data

    @staticmethod
    def read_data2(file_path):
        datalist = xfile.read(file_path).excel_to_dict(sheet=0)
        print(datalist)
        return datalist

    @staticmethod
    def read_data3(file_path):
        ex = Excel(file_path)
        ex.sheet_name = "Sheet1"
        ls_data = ex.get_key_value_list_to_list(start=1)
        js_data = ex.get_key_value_list_to_json(start=1)
        tp_data = ex.get_key_value_list_to_tuple(start=1)
        print(ls_data)
        print(js_data)
        print(tp_data)
        return ls_data

    @staticmethod
    def read_data4(file_path):
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=0)

        # Convert the DataFrame to a dictionary
        data_dict = df.to_dict()

        print(data_dict)
        return data_dict

