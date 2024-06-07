import pandas as pd
import sqlite3

db_connection = sqlite3.connect('trakt_data.db')

genre = pd.read_sql_query("SELECT COUNT(DISTINCT trakt_id) FROM dim_genres", con=db_connection)

# print(db_connection.execute("SELECT COUNT(DISTINCT trakt_id) FROM dim_genres"))
print(genre.drop_duplicates())