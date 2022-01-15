import logging
from xlsxwriter import Workbook

class CreateExcelFile():
    def __init__(self, data:list, name_of_table:str):
        self.data = data
        self.name_of_table = name_of_table

    def format_excel_file(self):
        if not self.data:
            return
        name_of_file = self.name_of_table + ".xlsx"
        name_of_sheet = self.name_of_table.split(',', 1)[1].lstrip()
        wb=Workbook(name_of_file)
        ws=wb.add_worksheet(name_of_sheet)
        bold = wb.add_format({'bold': True})
        ws.set_column('A:A', 40)
        
        col = 0
        row = 0
        for city in self.data:
            for key, value in city.items():
                if key == "City":
                    ws.write(row, col, value, bold)
                    row+=1
                else:
                    if key == 'published_at':
                        key = 'Published at'
                    ws.write(row, col, key)
                    ws.write(row, col +1, value)
                    row+=1
            row+= 2
    

        wb.close()
        logging.info(f"Excel file {name_of_file} created")
