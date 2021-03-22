from .wikipedia_scraper import WikipediaScraper
from .pfaf_scraper      import PFAFScraper

from pprint import pprint

class PlantScraper:
    def __init__(self, mongo):
        self.wiki  = WikipediaScraper()
        self.pfaf  = PFAFScraper()
        self.care  = mongo.plants.care

    def get(self, term):
        result = self.care.find_one(dict(name=term))
        if result is None:
            pfaf = self.pfaf.get(term)
            wiki = self.wiki.get(term)

            summary = wiki['summary'].lower()
            best = pfaf[0]
            for entry in pfaf:
                if entry['latin_name'].strip().lower() in summary:
                    best = entry
                    break

            result = dict(name=term,
                          summary=wiki['summary'],
                          **best)
            self.care.insert_one(result)
        return result

