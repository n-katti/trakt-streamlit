import requests
import json
from requests.structures import CaseInsensitiveDict

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

    def get_recommended_shows(self):
        params = {
        "ignore_collected" : "false",
        "ignore_watchlisted" : "false"
    }
        response = requests.get("https://api.trakt.tv/recommendations/shows", params=params, headers=self.all_headers)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(response)
