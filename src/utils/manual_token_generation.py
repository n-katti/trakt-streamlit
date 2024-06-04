
import sys
from dotenv import load_dotenv
import yaml
import os
from pathlib import Path
from trakt_api import Trakt

def load_config(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def execute():
    # Set up environment
    os.chdir(Path(__file__).parent.parent.parent)
    load_dotenv()

    config = load_config('config.yaml')
    url = config['api']['url']
    client_id = os.getenv(config['api']['client_id'])
    client_secret = os.getenv(config['api']['client_secret'])
    content_type = config['api']['headers']['content_type']
    api_version = config['api']['headers']['api_version']

    api = Trakt(client_id=client_id, client_secret=client_secret, content_type=content_type)
    # print(api.all_headers)
    device_code, user_code, verification_url = api.get_device_token()
    if device_code:
        print(f'Go to {verification_url} and enter the code {user_code}')
        proceed = input('Once done, enter Y to proceed. Proceed? [Y/N] ')
        if proceed == 'Y' or proceed == 'y':
            
            access_token, refresh_token, expires_in = api.get_access_token(code=device_code)
            print(f'Access Token: {access_token}')
            print(f'Refresh Token: {refresh_token}')
            print(f'These will expire in {expires_in} seconds')
        else:
            print('Breaking script.')

if __name__ == '__main__':
    execute()
