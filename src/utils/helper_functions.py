import yaml
import os
from dotenv import load_dotenv

def load_config(filename, env_path):
    os.chdir(env_path)
    load_dotenv()
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
        return parse_config(config=config)
    
def parse_config(config):
    config_values = {
                    "url" : config['api']['url'],
                    "client_id" : os.getenv(config['api']['client_id']),
                    "client_secret" : os.getenv(config['api']['client_secret']),
                    "access_token" : os.getenv(config['api']['tokens']['access_token']),
                    "refresh_token" : os.getenv(config['api']['tokens']['refresh_token']),
                    "token_last_updated_on" : os.getenv(config['api']['tokens']['token_last_updated_on']),
                    "content_type" : config['api']['headers']['content_type'],
                    "api_version" : config['api']['headers']['api_version']
                    }

    return config_values