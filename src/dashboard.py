import sqlite3
import streamlit as st
import pandas as pd
import os
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.realpath(__file__).split("trakt-streamlit")[0]+"trakt-streamlit")
from src.utils.logger_config import *
from pathlib import Path

cwd = Path(__file__).parent.parent
os.chdir(cwd)

def fetch_table_data(table_name, cursor):
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall() 
    data = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
    return data


conn = sqlite3.connect('trakt_data.db')

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
logger.info("Table names read from database")

tables = [table[0] for table in cursor.fetchall()]

selected_table = st.selectbox("Select a Table", tables)

if selected_table:
    st.write(f"### Data from {selected_table} table:")
    table_data = fetch_table_data(selected_table, cursor=cursor)
    st.write(table_data)

cursor.close()
conn.close()