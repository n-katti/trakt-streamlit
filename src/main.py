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
config_values = helper.load_main_config('config.yaml', cwd)
url = config_values['url']
client_id = config_values['client_id']
client_secret = config_values['client_secret']
access_token = config_values['access_token']
refresh_token = config_values['refresh_token']
token_last_updated_on = config_values['token_last_updated_on']
all_headers = config_values['all_headers']
token_headers = config_values['token_headers']


endpoints = config_values['endpoints']
# print(endpoints)
# Set up Trakt class
api = Trakt(client_id=client_id, client_secret=client_secret, access_token=access_token, all_headers=all_headers, token_headers=token_headers)

test = api.api('Recommended Shows', endpoints)
print(test)

# # Pull and process data from Trakt's recommended shows endpoint
# response = api.get_recommended_shows(results_to_return=300)
# recommended_shows_df, recommended_shows_genre = api.process_recommended_shows(response) # This returns two dfs: 1) all recommended shows and 2) their corresponding genres (since this is a 1:many relationship)
# # helper.dump_json(cwd, 'recommended_shows', response) # For testing, dump the JSON file 
# # test = helper.read_json(cwd, 'recommended_shows') # For testing, read the JSON file 
# helper.write_table('recommended_shows', recommended_shows_df)
# helper.write_table('recommended_shows_genres', recommended_shows_genre)

# response = api.get_history()
# # helper.dump_json(cwd, 'history', response) # For testing, dump the JSON file 
# # test = helper.read_json(cwd, 'history') # For testing, read the JSON file 
# movie_history_df, episode_history_df, show_history_df, genre_history_df = api.process_history(response)
# helper.write_table('raw_movie_history', movie_history_df)
# helper.write_table('raw_episode_history', episode_history_df)
# helper.write_table('raw_show_history', show_history_df)
# helper.write_table('raw_genre_history', genre_history_df)


