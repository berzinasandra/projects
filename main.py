from get_data import GetData
from create_excel_file import CreateExcelFile

class ProcessData():
    def __init__(self):
        data, name_of_table = self._get_data()
        user_input = input(f'-Create Excel file - 1\n-Create data visualisation - 2\nChoose operation: ')
        if user_input == '1':
            import pdb;pdb.set_trace()
            self.create_excel_file(data, name_of_table)
        elif user_input == '2':
            self.create_data_visualization(data)
        
    def _get_data(self):
        # always crawl data
        return GetData().run()

    def create_excel_file(self, data, name_of_table):
        # call for create_excel_file.py 
        CreateExcelFile(data, name_of_table).format_excel_file()

    def create_data_visualization(self, data):
        ...
        # call for data_vis_file



if __name__ == "__main__":
    ProcessData()
    
