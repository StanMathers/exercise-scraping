import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

class SimpleQueries:
    
    def create_table(self):
        self.c.execute(f'''
                       CREATE TABLE IF NOT EXISTS {self.tb_name}(
                           name TEXT,
                           discount TEXT,
                           old_price TEXT,
                           new_price TEXT,
                           release_date TEXT
                       )
                       ''')
        self.conn.commit()
    
    def query(self):
        return pd.read_sql_query(f'SELECT * FROM {self.tb_name}',
                                 self.conn)
    
    def number_of_records(self):
        self.c.execute(f'SELECT * FROM {self.tb_name}')
        return len(self.c.fetchall())
    
    def trunc_table(self):
        self.c.execute(f'DELETE FROM {self.tb_name}')
        self.conn.commit()

class SteamParsing(SimpleQueries):
    def __init__(self, html: str, db_name: str = None, tb_name: str = None):
        self.soup = BeautifulSoup(html, 'lxml')
        
        self.db_name = db_name
        self.tb_name = tb_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.create_table()
    
    def product_names(self):
        return [i.text for i in self.soup.find_all('span', attrs={'class': 'title'})]

    def product_discount(self):
        return [i.span.text for i in self.soup.find_all('div', attrs={'class': 'col search_discount responsive_secondrow'})]
    
    def product_old_price(self):
        return [i.span.strike.text for i in self.soup.find_all('div', attrs={'class': 'col search_price discounted responsive_secondrow'})]
    
    def product_new_price(self):
        return [i.br.next_element.strip() for i in self.soup.find_all('div', attrs={'class': 'col search_price discounted responsive_secondrow'})]
    
    def product_release_date(self):
        return [i.text if len(i.text) > 0 else 'N/A' for i in self.soup.find_all('div', attrs={'class': 'col search_released responsive_secondrow'})]

    def to_dataframe(self):
        consist = {
            'name': self.product_names(),
            'discount': self.product_discount(),
            'old price': self.product_old_price(),
            'new price': self.product_new_price(),
            'release date': self.product_release_date()
        }
        df = pd.DataFrame(consist)
        return df
    
    def to_sql(self):
        data = zip(self.product_names(), self.product_discount(),
                   self.product_old_price(), self.product_new_price(),
                   self.product_release_date())
        self.c.executemany(f'INSERT INTO {self.tb_name} VALUES (?, ?, ?, ?, ?)', data)
        self.conn.commit()
