import pandas as pd
from pathlib import Path
import sqlite3 as sql
from dotenv import load_dotenv
import yaml
import os
from utils.trakt_api import Trakt
import utils.helper_functions as helper
import requests
import json


# Set up environment
cwd = Path(__file__).parent.parent
os.chdir(cwd)

# Load all variables
config_values = helper.load_config('config.yaml', cwd)
url = config_values['url']
client_id = config_values['client_id']
client_secret = config_values['client_secret']
api_version = config_values['api_version']
content_type = config_values['content_type']
access_token = config_values['access_token']
refresh_token = config_values['refresh_token']
token_last_updated_on = config_values['token_last_updated_on']

# Set up Trakt class
api = Trakt(client_id=client_id, client_secret=client_secret, content_type=content_type, access_token=access_token, api_version=api_version)

# Pull and process data from Trakt's recommended shows endpoint
response = api.get_recommended_shows(results_to_return=300)
recommended_shows_df, recommended_shows_genre = api.process_recommended_shows(response) # This returns two dfs: 1) all recommended shows and 2) their corresponding genres (since this is a 1:many relationship)
# helper.dump_json(cwd, 'recommended_shows', response) # For testing, jump the JSON file 
helper.write_table('recommended_shows', recommended_shows_df)
helper.write_table('recommended_shows_genres', recommended_shows_genre)