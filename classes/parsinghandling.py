import pandas as pd
from bs4 import BeautifulSoup

class SteamParsing:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, 'lxml')
    
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
