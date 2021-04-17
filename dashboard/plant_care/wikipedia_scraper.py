import wikipedia
from pprint import pprint

import json, os

class WikipediaScraper:
    def __init__(self):
        pass

    def get(self, term):
        try:
            results = wikipedia.search(term)
            if len(results) == 0:
                raise RuntimeError(f'No wikipedia page for: {term}')
            best_page = wikipedia.page(results[0], auto_suggest=False)
            return dict(title=best_page.title, summary=best_page.summary)
        except wikipedia.DisambiguationError as e:
            return dict(title=term, summary='No summary could be found as the plant name is ambiguous. Try supplying a more specific plant name, such as "Peppermint" instead of "Mint", or even the latin name, "Mentha piperita," to improve results.')

