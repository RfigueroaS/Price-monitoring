from pipeline import *
import logging

try:
    data = scrape_amazon("https://www.amazon.com.mx/")
except Exception as e:
    logging.error(f"Error al scrapear: {e}")