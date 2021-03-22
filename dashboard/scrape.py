from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from time import time
from pprint import pprint

import json, os

fields = ['latin_name', 'common_name', 'habitat', 'height', 'hardiness', 'growth', 'soil', 'shade', 'moisture', 'edible', 'medicinal', 'other']
key = dict(growth=dict(S='slow', M='medium', F='fast'),
           soil=dict(L='light', M='medium', H='heavy'),
           pH=dict(A='acidic', N='neutral', B='basic'),
           shade=dict(F='full', S='semi', N='none'),
           moisture=dict(D='dry', M='moist', We='wet', Wa='water'))


class PlantScraper:
    def __init__(self):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(options=op)
        self.wait = WebDriverWait(self.driver, 10)

    def search(self, term):
        self.driver.get('https://pfaf.org/user/Default.aspx')
        self.driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$txtSearch').send_keys(term + Keys.RETURN)
        table = self.wait.until(presence_of_element_located((By.ID, 'ContentPlaceHolder1_gvresults')))
        rows = table.find_elements(By.TAG_NAME, 'tr')
        plants = []
        for row in rows:
            plant = dict()
            col = row.find_elements(By.TAG_NAME, 'td')
            for k, cell in zip(fields, col):
                plant[k] = cell.text
            plants.append(plant)
        return plants

    def expand(self, plant):
        pass

if os.path.isfile('plant.json'):
    with open('plant.json', 'r') as infile:
        plants = json.load(infile)
        pprint(plants)
else:
    scraper = PlantScraper()
    plants = scraper.search('Radish')
    with open('plant.json', 'w') as outfile:
        json.dump(plants, outfile)
    pprint(plants)
