from datetime import datetime
from mysql.connector import connect
from dotenv import load_dotenv
import os

load_dotenv()

def _establish_connection():
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE =  os.getenv('MYSQL_DATABASE')

    mydb = connect(
    host= MYSQL_HOST, 
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
    return mydb

def insert_data_of_city(data):
    mydb = _establish_connection()
    mycoursor =  mydb.cursor()
    mycoursor.execute(INSERT_DATA_IN_CITIES_DATA,(
        data.get('City'),
        datetime.now(),
        data.get('published_at'),
        data.get('Number of establishments'),
        data.get('Number of bedrooms'),
        data.get('Occupancy rate of bedrooms, %'),
        data.get('Change compared to previous year, %-units'),
        data.get('Room price, euros (incl. VAT 10 %)'),
        data.get('RevPAR, euros (incl. VAT 10 %)'))
        )
    
    mydb.commit()
    mydb.close()

INSERT_DATA_IN_CITIES_DATA = """
    INSERT INTO cities_data (city, created_at, published_at, nr_of_establishments, nr_of_bedrooms, occupancy_rate_bedroom, change_per_year , room_price , RevPAR)
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    );
"""
