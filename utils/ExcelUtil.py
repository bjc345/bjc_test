import os
from utils.logUtil import mylog
import xlrd
mylog=mylog()

class SheetTypeError(Exception):
    pass
class ExcelReader:
    def __init__(self,excel_file,sheet_by):
        if os.path.exists(excel_file):
            self.excel_file=excel_file
        else:
            mylog.error('文件名不存在')
        self.sheet_by=sheet_by
        self._data=list()
    def data(self):
        if not  self._data:
            workbook=xlrd.open_workbook(self.excel_file)
            if not isinstance(self.sheet_by,(int,str)):
                raise SheetTypeError('请输入Int or Str')
            if isinstance(self.sheet_by,str):
                sheet=workbook.sheet_by_name(self.sheet_by)

            if isinstance(self.sheet_by,int):
                sheet=workbook.sheet_by_index(self.sheet_by)
            title=sheet.row_values(0)
            self._data=[dict(zip(title,sheet.row_values(col))) for col in range(1,sheet.nrows)]

        return self._data

if __name__=="__main__":
    print(ExcelReader('../test_case.xlsx',0).data())

