import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()


gmaps_key = googlemaps.Client(key = os.getenv('GMAPS_KEY'))