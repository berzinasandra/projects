import logging
import mysql.connector
from dotenv import load_dotenv
import os
# from database import INSERT

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_USER')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE =  os.getenv('MYSQL_DATABASE')



class CreateExcelFile():
    # def __init__(self):
    #     self.data = data

     

    def connect(self):
        mydb = mysql.connector.connect(
            host= MYSQL_HOST, 
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        import pdb;pdb.set_trace()

        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS mydatabase")

        
    

if __name__ == '__main__':
     CreateExcelFile().connect()