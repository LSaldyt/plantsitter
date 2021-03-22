import wikipedia
from pprint import pprint

import json, os

class WikipediaScraper:
    def __init__(self):
        pass

    def get(self, term):
        results = wikipedia.search(term)
        if len(results) == 0:
            raise RuntimeError(f'No wikipedia page for: {term}')
        for result in results:
            try:
                best_page = wikipedia.page(result, auto_suggest=False)
                print(best_page.title)
                print(best_page.content)
                return best_page
            except Exception as e:
                print(e)
                continue


scraper = WikipediaScraper()
page    = scraper.get('Radish')
