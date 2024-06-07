import streamlit as st
import sqlite3

connection = sqlite3.connect('trakt_data.db')
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

tables = cursor.fetchall() 

print(tables)