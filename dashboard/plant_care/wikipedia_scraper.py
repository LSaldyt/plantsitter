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
        best_page = wikipedia.page(results[0], auto_suggest=False)
        return dict(title=best_page.title, summary=best_page.summary)
