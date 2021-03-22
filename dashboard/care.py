import patch
from plant_care.plant_scraper import PlantScraper
from utils.mongo import MongoDatabases

mongo   = MongoDatabases('plants')
scraper = PlantScraper(mongo)
scraper.get('Basil')
