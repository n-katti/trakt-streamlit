import yaml
import os
from dotenv import load_dotenv
import json
from pathlib import Path
import sqlite3
import pandas as pd
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.realpath(__file__).split("trakt-streamlit")[0]+"trakt-streamlit")
from src.utils.trakt_api import *
from src.utils.logger_config import *

db_connection = sqlite3.connect('trakt_data.db')

def load_main_config(filename, env_path):
    load_dotenv()
    with open(env_path / filename, 'r') as file:
        config = yaml.safe_load(file)
        return parse_main_config(config=config)
    
def parse_main_config(config):
    access_token = os.getenv(config['tokens']['access_token'])
    client_id = os.getenv(config['client_id'])
    all_headers = config['all_headers']
    all_headers['Authorization'] = str.replace(all_headers['Authorization'], "TOKEN_REPLACE_STRING", access_token)
    all_headers['trakt-api-key'] = client_id
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

def write_table(table_name, df, connection = db_connection, if_exists='replace'):

    # Write DataFrame to SQLite table
    df.to_sql(name=table_name, con=connection, if_exists=if_exists, index=False)

    # Close connection if it was established inside the function
    # if connection is not None:
    #     connection.close()

def merge_and_write_tables(input_table_names, new_table_name, if_exists='replace', drop_duplicates=False, connection = db_connection):
    union_query = ' UNION '.join(f'SELECT * FROM {table_name}' for table_name in input_table_names)

    try:
        union_df = pd.read_sql_query(union_query, connection)
        write_table(new_table_name, union_df, if_exists=if_exists)
        logger.info(f'Unioned and inserted successfully to {new_table_name}')
    except Exception as e:
        logger.error(f'Failed to union/insert. Eror message: {e}')

def close_db_connection(connection = db_connection):
    connection.close()


    

