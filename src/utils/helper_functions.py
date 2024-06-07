import yaml
import os
from dotenv import load_dotenv
import json
from pathlib import Path
import sqlite3
import pandas as pd

def load_main_config(filename, env_path):
    load_dotenv()
    with open(env_path / filename, 'r') as file:
        config = yaml.safe_load(file)
        return parse_main_config(config=config)
    
def parse_main_config(config):
    access_token = os.getenv(config['tokens']['access_token'])
    all_headers = config['all_headers']
    all_headers['Authorization'].format(trakt_access_token=access_token)
    config_values = {
                    "url" : config['url'],
                    "client_id" : os.getenv(config['client_id']),
                    "client_secret" : os.getenv(config['client_secret']),
                    "access_token" : access_token,
                    "refresh_token" : os.getenv(config['tokens']['refresh_token']),
                    "token_last_updated_on" : os.getenv(config['tokens']['token_last_updated_on']),
                    "all_headers" : all_headers,
                    "token_headers" : config['token_headers'],
                    "endpoints" : config['endpoints']
                    }
    
    return config_values

def dump_json(env_path, file_name, data):
    output_path = env_path / 'samples' / f"{file_name}.json"
    with open(output_path, 'w') as file:
         json.dump(data, file, indent=4)

def read_json(env_path, file_name):
    input_path = env_path / 'samples' / f"{file_name}.json"
    try:
        with open(input_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {input_path}")
        return None 
    
def create_sql_connection(database_name):
    return sqlite3.connect(database_name)

def write_table(table_name, df, connection = None, if_exists='replace'):

    if connection is None:
        connection = sqlite3.connect('trakt_data.db')

    # Write DataFrame to SQLite table
    df.to_sql(name=table_name, con=connection, if_exists=if_exists, index=False)

    # Close connection if it was established inside the function
    if connection is not None:
        connection.close()
