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

config_values = helper.load_config('config.yaml', cwd)
url = config_values['url']
client_id = config_values['client_id']
client_secret = config_values['client_secret']
api_version = config_values['api_version']
content_type = config_values['content_type']
access_token = config_values['access_token']
refresh_token = config_values['refresh_token']
token_last_updated_on = config_values['token_last_updated_on']


# # Function to load in YAML file,
# def load_config(filename):
#     with open(filename, 'r') as file:
#         return yaml.safe_load(file)
    
# def parse_config(config):
#     url = config['api']['url']
#     client_id = os.getenv(config['api']['client_id'])
#     client_secret = os.getenv(config['api']['client_secret'])
#     content_type = config['api']['headers']['content_type']
#     api_version = config['api']['headers']['api_version']

#     return url, client_id, client_secret, content_type, api_version

# if __name__ == '__main__':
#     config = load_config('config.yaml')

#     url, client_id, client_secret, content_type, api_version = parse_config(config=config)
#     headers = {
#     "Content-Type": "application/json",  # Example header
#     "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Example header for authentication
# }

api = Trakt(client_id=client_id, client_secret=client_secret, content_type=content_type, access_token=access_token, api_version=api_version)
api.get_recommended_shows()

# headers = {
#     "Content-Type": "application/json",  # Example header
#     "trakt-api-version" : "2",
#     "trakt-api-key" : f"{client_id}"
# }

# params = {
#     "type" : "movies"
# }
# response = requests.get('https://api.trakt.tv/countries/movies', params=params, headers=headers) 

# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print('API request failed:', response.status_code)


