import logging
import pandas as pd
from lxml import html
import requests
from datetime import datetime
from database import insert_data_of_city


class GetData:
    def __init__(self):
        self.url = "https://www.stat.fi/til/matk/tau_en.html"
        self.newest_data_table_name = None
    def run(self):
        self._get_tree_from_page()
        url = self._get_newest_data_url()
        if not url:
            print('Nop')
            logging.info("Could not get url for newest data table")
            # return
        # data = self._pick_data_of_cities(url)
        
        data = [{'City': 'Espoo', 'published_at': '2021-09-01', 'Number of establishments': 14, 'Number of bedrooms': 1503, 'Occupancy rate of bedrooms, %': 45.9, 'Change compared to previous year, %-units': 8.7, 'Room price, euros (incl. VAT 10 %)': '75.84', 'RevPAR, euros (incl. VAT 10 %)': '34.78'}]
        self._store_data_in_db(data)

        return data, self.newest_data_table_name

    def _get_tree_from_page(self):
        page=requests.get(self.url)  
        page_content = page.content
        self.tree = html.fromstring(page_content)

    def _get_newest_data_url(self):
        full_url = None
        try:
            self.newest_data_table_name = self.tree.xpath("(//a[contains(text(), 'Appendix table 3.1. Hotel capacity and capacity utilization')])[1]//parent::a/text()")[0]
            self.published_at_date = self._get_published_date()
            logging.info(f"Accesing table -  {self.newest_data_table_name}")
            raw_url = self.tree.xpath("(//a[contains(text(), 'Appendix table 3.1. Hotel capacity and capacity utilization')])[1]//parent::a")[0].attrib
            url = raw_url.get("href")
            full_url = "https://www.stat.fi"+url
        except Exception as e:
            logging.info(f"Failed to access newest data table")
            return
        return full_url

    def _get_published_date(self):
        date = self.newest_data_table_name.split(',', 1)[1].lstrip()
        return datetime.strptime(date, '%B %Y').strftime('%Y-%m-%d')

    def _pick_data_of_cities(self, url:str):
        df = pd.read_html(url)
        if not df:
            logging.info("Failed to get data frame")
            return

        data = df[0].to_dict('records')

        data = self._select_cities(data)
        ordered_data = self._order_data(data)
        return ordered_data

    def _order_data(self, data:list):
        key_order = ['City', 'Number of establishments', 'Number of bedrooms', 'Occupancy rate of bedrooms, %', 'Change compared to previous year, %-units', 'Room price, euros (incl. VAT 10 %)', 'RevPAR, euros (incl. VAT 10 %)']
        ordered_data=[]
        for city in data:
            new_city= {}
            for k in key_order:
                new_city[k] = city.get(k)
                new_city['published_at'] = self.published_at_date
            ordered_data.append(new_city)
        return ordered_data
    
    def _select_cities(self, data:list):
        cities = [
            "Whole country",
            "Helsinki",
            "Espoo",
            "Vantaa",
            "Tampere",
            "Oulu",
            "Rovaniemi",
            "Turku",
            "Kuopio",
            "Jyväskylä"
        ]
        needed_cities= []

        for city in data:
            if city.get("Region / municipality") in cities:
                city["City"] = city.pop("Region / municipality")
                needed_cities.append(city)

        return needed_cities

    def _store_data_in_db(self, data):
        for d in data:
            if d.get("City") == 'Whole country':
                continue
            else:
                insert_data_of_city(d)
