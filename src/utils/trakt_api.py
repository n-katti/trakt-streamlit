import requests
import json
from requests.structures import CaseInsensitiveDict
import pandas as pd

class Trakt:
    def __init__ (self, client_id, client_secret, content_type, access_token=None, api_version=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_headers = {"Content-Type" : f"{content_type}"}
        self.all_headers =  {
                            "Content-Type" : f"{content_type}",  
                            "Authorization" : f"Bearer {access_token}",
                            "trakt-api-key" : f"{client_id}",
                            "trakt-api-version" : f"{api_version}"
                            }

    def get_device_token(self):

        values = {
        "client_id": f"{self.client_id}"
        }

        response = requests.post('https://api.trakt.tv/oauth/device/code', params=values, headers=self.token_headers)

        if response.status_code == 200:
            data = response.json()
            device_code = data['device_code']
            user_code = data['user_code']
            verification_url = data['verification_url']
            
            return device_code, user_code, verification_url

        else:
            print('API request failed:', response.status_code)
            return None

    def get_access_token(self, code):
        values = {
            "code": f"{code}",
            "client_id": f"{self.client_id}",
            "client_secret": f"{self.client_secret}",
            }
        
        response = requests.post('https://api.trakt.tv/oauth/device/token', params=values, headers=self.token_headers) 

        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            refresh_token = data['refresh_token']
            expires_in = data['expires_in']
            return access_token, refresh_token, expires_in
        else:
            print('API request failed:', response.status_code)

    def handle_response(self, input):
        if input.status_code == 200:
            data = input.json()
        else:
            data = f"Error message from API: {input}"
        return data     
    

    def api_call(self, url, params, header, max_pages=None, max_results=100):
        all_results = []
        page = 1
        total_results = 0

        while True:
            if max_pages is not None and page > max_pages:
                break
            if total_results >= max_results:
                break

            remaining_results = max_results - total_results
            current_limit = min(100, remaining_results)

            api_params = params.copy()
            api_params['page'] = f"{page}"
            api_params['limit'] = f"{current_limit}"

            try:
                response = requests.get(url, params=api_params, headers=header)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                data = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error occurred during API call: {e}")
                return None  # Return None to indicate failure

            if not response:
                break

            all_results.extend(data)
            total_results += len(data)

            if len(data) < current_limit:
                break
            
            page += 1

        return all_results

            

    def get_recommended_shows(self, ignore_collected = "true", ignore_watchlisted = "false", extended="full", results_to_return=220):

        params =  {           
            "ignore_collected" : f"{ignore_collected}",
            "ignore_watchlisted" : f"{ignore_watchlisted}",
            "extended" : f"{extended}"
        }

        url = "https://api.trakt.tv/recommendations/shows"

        results = self.api_call(url=url, params=params, header=self.all_headers, max_results=results_to_return)

        return results

    def process_recommended_shows(self, data) -> pd.DataFrame:
        all_show_data = []
        all_genre_data = []

        for show in data:
            show_data = {
                'title': show.get('title'),
                'year': show.get('year'),
                'trakt_id': show.get('ids', {}).get('trakt'),
                'imdb_id': show.get('ids', {}).get('imdb'),
                'slug_id': show.get('ids', {}).get('slug'),
                'tvdb_id': show.get('ids', {}).get('tvdb'),
                'tmdb_id': show.get('ids', {}).get('tmdb'),
                'tagline': show.get('tagline'),
                'overview': show.get('overview'),
                'first_aired': show.get('first_aired'),
                'runtime': show.get('runtime'),
                'country': show.get('country'),
                'trailer': show.get('trailer'),
                'homepage': show.get('homepage'),
                'status': show.get('status'),
                'rating': show.get('rating'),
                'votes': show.get('votes'),
                'comment_count': show.get('comment_count'),
                'aired_episodes': show.get('aired_episodes')
                # Add more fields as needed
            }

            all_show_data.append(show_data)

            for genre in show.get('genres'):

                show_genres = {
                    'trakt_id': show.get('ids', {}).get('trakt'),
                    'genre' : genre
                }

                all_genre_data.append(show_genres)

        show_df = pd.DataFrame(all_show_data)
        genre_df = pd.DataFrame(all_genre_data)

        return show_df, genre_df
        


        
