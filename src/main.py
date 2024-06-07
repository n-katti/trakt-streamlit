import pandas as pd
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import sqlite3 as sql
from dotenv import load_dotenv
import yaml
import os
from utils.trakt_api import Trakt
from utils.omdb_api import OMDB
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

##################################
# 1) Pull data from Trakt API
##################################

# Set up Trakt class
# api = Trakt(client_id=client_id, client_secret=client_secret, access_token=access_token, all_headers=all_headers, token_headers=token_headers)

# # Pull recommended shows
# response = api.api_call('Recommended Shows', endpoints)
# recommended_shows_df, recommended_shows_genre = api.process_recommended_shows(response) # This returns two dfs: 1) all recommended shows and 2) their corresponding genres (since this is a 1:many relationship)
# # # helper.dump_json(cwd, 'recommended_shows', response) # For testing, dump the JSON file 
# # # test = helper.read_json(cwd, 'recommended_shows') # For testing, read the JSON file 
# helper.write_table('raw_recommended_shows', recommended_shows_df)
# helper.write_table('raw_recommended_shows_genres', recommended_shows_genre)

# # Pull movie and tv history
# response = api.api_call('History', endpoints)
# # # helper.dump_json(cwd, 'history', response) # For testing, dump the JSON file 
# # # test = helper.read_json(cwd, 'history') # For testing, read the JSON file 
# movie_history_df, episode_history_df, show_history_df, genre_history_df = api.process_history(response)

# helper.write_table('raw_movie_history', movie_history_df)
# helper.write_table('raw_episode_history', episode_history_df)
# helper.write_table('raw_show_history', show_history_df)
# helper.write_table('raw_genre_history', genre_history_df)

# # Merge both genre tables and drop any duplicates
# helper.merge_and_write_tables(['raw_genre_history', 'raw_recommended_shows_genres'], 'dim_genres')

##################################
# 2) Pull movie/tv posters from OMDB API 
##################################
omdb_key = config_values['omdb_key']
omdb_url = config_values['omdb_url']

omdb_api = OMDB(omdb_key, omdb_url)
# print(omdb_key)
posters_df = omdb_api.api_call(['tt1475582', 'tt0141842', 'tt0306414'])

helper.write_table('dim_posters', posters_df, if_exists='append')

# # # Close the connection
helper.close_db_connection()