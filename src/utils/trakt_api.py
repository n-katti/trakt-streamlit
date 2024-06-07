import requests
import json
from requests.structures import CaseInsensitiveDict
import pandas as pd

class Trakt:
    def __init__ (self, client_id, client_secret, token_headers, all_headers=None, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_headers = token_headers
        self.all_headers =  all_headers

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
    

    def api_call(self, name, config):
        all_results = []
        page = 1
        total_results = 0
        url = config[name]['url']
        params = config[name]['params']

        if config[name]['headers'] == 'all':
            headers = self.all_headers
        else:
            headers = self.token_headers
        
        if not config[name]['results_to_return']:
            max_results = 100
        else:
            max_results = config[name]['results_to_return']

        try:
            max_pages = config[name]['max_pages']
        
        except:
            max_pages = None
        
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
                response = requests.get(url, params=api_params, headers=headers)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                data = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error occurred during API call: {e}")
                print(headers)
                print(params)
                return None  # Return None to indicate failure

            if not response:
                break

            all_results.extend(data)
            total_results += len(data)

            if len(data) < current_limit:
                break
            
            page += 1

        return all_results

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

    def process_history(self, data) -> pd.DataFrame:
        all_movie_data = []
        all_episode_data = []
        all_show_data = []
        all_genre_data = []

        

        for media in data:
            type = media['type']
            if type == 'movie':
                movie_data = {
                            'id' : media.get('id', {}),
                            'watched_at' : media.get('watched_at', {}),
                            'action' : media.get('action', {}),
                            'type' : media.get('type', {}),
                            'title': media.get(type, {}).get('title'),
                            'year': media.get(type, {}).get('year'),
                            'trakt_id': media.get(type, {}).get('ids').get('trakt'),
                            'imdb_id': media.get(type, {}).get('ids').get('imdb'),
                            'slug_id': media.get(type, {}).get('ids').get('slug'),
                            'tvdb_id': media.get(type, {}).get('ids').get('tvdb'),
                            'tmdb_id': media.get(type, {}).get('ids').get('tmdb'),
                            'tagline': media.get(type, {}).get('tagline'),
                            'overview': media.get(type, {}).get('overview'),
                            'released': media.get(type, {}).get('released'),
                            'runtime': media.get(type, {}).get('runtime'),
                            'country': media.get(type, {}).get('country'),
                            'rating': media.get(type, {}).get('rating'),
                            'votes': media.get(type, {}).get('votes'),
                            'comment_count': media.get(type, {}).get('comment_count'),
                            'trailer': media.get(type, {}).get('trailer'),
                            'homepage': media.get(type, {}).get('homepage'),
                            'certification': media.get(type, {}).get('certification')
                            }
                            
                all_movie_data.append(movie_data)

            
            if type == 'episode':
                episode_data = {
                            'id' : media.get('id', {}),
                            'show_trakt_id' : media.get('show', {}).get('ids').get('trakt'),
                            'watched_at' : media.get('watched_at', {}),
                            'action' : media.get('action', {}),
                            'type' : media.get('type', {}),
                            'title': media.get(type, {}).get('title'),
                            'season': media.get(type, {}).get('season'),
                            'episode': media.get(type, {}).get('number'),
                            'trakt_id': media.get(type, {}).get('ids').get('trakt'),
                            'imdb_id': media.get(type, {}).get('ids').get('imdb'),
                            'slug_id': media.get(type, {}).get('ids').get('slug'),
                            'tvdb_id': media.get(type, {}).get('ids').get('tvdb'),
                            'tmdb_id': media.get(type, {}).get('ids').get('tmdb'),
                            'tagline': media.get(type, {}).get('tagline'),
                            'overview': media.get(type, {}).get('overview'),
                            'released': media.get(type, {}).get('first_aired'),
                            'runtime': media.get(type, {}).get('runtime'),
                            'rating': media.get(type, {}).get('rating'),
                            'votes': media.get(type, {}).get('votes'),
                            'comment_count': media.get(type, {}).get('comment_count')
                            }

                all_episode_data.append(episode_data)

                show_data = {
                            'title': media.get('show', {}).get('title'),
                            'year': media.get('show', {}).get('year'),
                            'trakt_id': media.get('show', {}).get('ids').get('trakt'),
                            'imdb_id': media.get('show', {}).get('ids').get('imdb'),
                            'slug_id': media.get('show', {}).get('ids').get('slug'),
                            'tvdb_id': media.get('show', {}).get('ids').get('tvdb'),
                            'tmdb_id': media.get('show', {}).get('ids').get('tmdb'),
                            'tagline': media.get('show', {}).get('tagline'),
                            'overview': media.get('show', {}).get('overview'),
                            'released': media.get('show', {}).get('first_aired'),
                            'runtime': media.get('show', {}).get('runtime'),
                            'certification': media.get('show', {}).get('certification'),
                            'country': media.get('show', {}).get('country'),
                            'status': media.get('show', {}).get('status'),
                            'rating': media.get('show', {}).get('rating'),
                            'votes': media.get('show', {}).get('votes'),
                            'comment_count': media.get('show', {}).get('comment_count'),
                            'trailer': media.get('show', {}).get('trailer'),
                            'homepage': media.get('show', {}).get('homepage'),
                            'network': media.get('show', {}).get('network'),
                            'aired_episodes': media.get('show', {}).get('aired_episodes'),
                            }
    
            if type == 'movie':
                genre_type = 'movie'
            else:
                genre_type = 'show'

            for genre in media.get(genre_type, {}).get('genres'):

                genres = {
                    'trakt_id': media.get(genre_type, {}).get('ids').get('trakt'),
                    'genre' : genre
                        }       

                all_genre_data.append(genres)

                all_show_data.append(show_data)

        movie_df = pd.DataFrame(all_movie_data)
        episode_df = pd.DataFrame(all_episode_data)
        show_df = pd.DataFrame(all_show_data).drop_duplicates()
        genre_df = pd.DataFrame(all_genre_data).drop_duplicates()

        return movie_df, episode_df, show_df, genre_df
    

    def api_call_deprecated(self, url, params, header, max_pages=None, max_results=100):
        '''
        Deprecated, use api_call for all other calls
        '''
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

            
    def get_history(self, extended="full", results_to_return=10000):
        '''
        Deprecated, use api_call method for all calls now
        '''

        params =  {           
            "extended" : f"{extended}"
        }

        url = "https://api.trakt.tv/sync/history"

        results = self.api_call(url=url, params=params, header=self.all_headers, max_results=results_to_return)

        return results
    
    def get_recommended_shows(self, ignore_collected = "true", ignore_watchlisted = "false", extended="full", results_to_return=300):
        '''
        Deprecated, use api_call method for all calls now
        '''
        params =  {           
            "ignore_collected" : f"{ignore_collected}",
            "ignore_watchlisted" : f"{ignore_watchlisted}",
            "extended" : f"{extended}"
        }

        url = "https://api.trakt.tv/recommendations/shows"

        results = self.api_call(url=url, params=params, header=self.all_headers, max_results=results_to_return)

        return results