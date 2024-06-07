import requests
import json
from requests.structures import CaseInsensitiveDict
import pandas as pd
import os
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.realpath(__file__).split("trakt-streamlit")[0]+"trakt-streamlit")
from src.utils.logger_config import *
from src.utils.helper_functions import dump_json, read_json
from pathlib import Path

cwd = Path(__file__).parent.parent.parent
os.chdir(cwd)

class OMDB: 
    def __init__ (self, apikey, url):
        self.apikey = apikey
        self.url = url

    
    def api_call(self, ids):
        all_data = []
        poster_data = []
        for id in ids:
            api_params = {                            
                            'apikey' : self.apikey,
                            'i' : f"{id}"
                         }
            
            try:
                response = requests.get(self.url, params=api_params)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                data = response.json()
                poster_url = {}
                poster_url['imdb_id'] = id
                poster_url['url'] = data['Poster']
                url = data['Poster']
                all_data.append(data)
                title = data.get('Title', {})
                logger.info(f"Poster URL for {title} (IMDb ID: {id}) has been downloaded successfully")

                
                save_folder = 'media'
                save_path = self.download_poster(id, title, url, save_folder)
                poster_url['save_path'] = save_path
                poster_data.append(poster_url)

            except requests.exceptions.RequestException as e:
                logger.error(f"Error occurred during API call: {e}")
                return None  # Return None to indicate failure

        poster_df = pd.DataFrame(poster_data)
        poster_df['save_path'] = poster_df['save_path'].astype(str)
        return poster_df
        # dump_json(cwd, 'posters', all_data)
        # dump_json(cwd, 'poster_url', poster_data)

    def download_poster(self, id, title, url, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_path = cwd / 'src' / directory / f"{id}.jpg"
        try:
            poster = requests.get(url)
            poster.raise_for_status()

            with open(save_path, "wb") as file:
                file.write(poster.content)
            
            logger.info(f"Poster for {title} (IMDb ID: {id}) has been downloaded successfully")
            return save_path

        except Exception as e:
            logger.error(f"Error downloading poster for {title} (IMDb ID: {id}): {e}")
            return None
    

# api = OMDB('410de39', 'http://www.omdbapi.com/?')

# api.api_call(['tt1475582', 'tt0141842'])

# posters_test = read_json(cwd, 'poster_url')

# for x in posters_test:
    # api.download_poster(x['imdb_id'], 'Sopranos', x['url'], 'Media')