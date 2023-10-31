import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

#Connection to the google API with our environment variables
gmaps_key = googlemaps.Client(key = os.getenv('GMAPS_KEY'))