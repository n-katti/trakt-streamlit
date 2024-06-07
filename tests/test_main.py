import pandas as pd
import sys
import os
import pytest
sys.path.append(os.path.realpath(__file__).split("trakt-streamlit")[0]+"trakt-streamlit")
from src.utils.trakt_api import *

def test_process_recommended_shows():
    '''
    Tests that the processing of the data returned from the Recommended Shows API endpoint is as expected
    '''
    api = Trakt('123', '123', '123')
    input = [{
            'title': 'The Mandalorian',
            'year': 2019,
            'ids': {
                'trakt': 137178,
                'slug': 'the-mandalorian',
                'tvdb': 361753,
                'imdb': 'tt8111088',
                'tmdb': 82856,
                'tvrage': None
            },
            'tagline': 'This is the way.',
            'overview': 'After the fall of the Galactic Empire, lawlessness has spread throughout the galaxy. A lone gunfighter makes his way through the outer reaches, earning his keep as a bounty hunter.',
            'first_aired': '2019-11-12T08:00:00.000Z',
            'airs': {
                'day': 'Friday',
                'time': '03:00',
                'timezone': 'America/New_York'
            },
            'runtime': 40,
            'certification': 'TV-14',
            'network': 'Disney+',
            'country': 'us',
            'trailer': 'https://youtube.com/watch?v=2RVnrBLOBcI',
            'homepage': 'http://www.disneyplus.com/series/the-mandalorian/3jLIGMDYINqD',
            'status': 'returning series',
            'rating': 8.453589800939387,
            'votes': 22355,
            'comment_count': 105,
            'updated_at': '2024-06-01T15:13:32.000Z',
            'language': 'en',
            'languages': ['en'],
            'available_translations': [
                'ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en', 'eo', 'es', 'et', 'fa', 'fi', 'fr', 'gl', 'he', 'hr', 'hu', 'it', 'ja', 'ka', 'ko', 'lt', 'lv', 'my', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sr', 'sv', 'th', 'tr', 'uk', 'vi', 'zh'
            ],
            'genres': ['fantasy', 'science-fiction', 'action', 'adventure', 'drama'],
            'aired_episodes': 24,
            'favorited_by': [],
            'recommended_by': []
            }]
    
    expected_genres = pd.DataFrame([
                                    {"trakt_id" : 137178, "genre" : "fantasy"}, 
                                    {"trakt_id" : 137178, "genre" : "science-fiction"}, 
                                    {"trakt_id" : 137178, "genre" : "action"},                                                                         
                                    {"trakt_id" : 137178, "genre" : "adventure"}, 
                                    {"trakt_id" : 137178, "genre" : "drama"}
                                    ])
    expected_details = pd.DataFrame([{
                    'title': 'The Mandalorian',
                    'year': 2019,
                    'trakt_id': 137178,
                    'imdb_id': 'tt8111088',
                    'slug_id': 'the-mandalorian',
                    'tvdb_id': 361753,
                    'tmdb_id': 82856,
                    'tagline': 'This is the way.',
                    'overview': 'After the fall of the Galactic Empire, lawlessness has spread throughout the galaxy. A lone gunfighter makes his way through the outer reaches, earning his keep as a bounty hunter.',
                    'first_aired': '2019-11-12T08:00:00.000Z',
                    'runtime': 40,
                    'country': 'us',
                    'trailer': 'https://youtube.com/watch?v=2RVnrBLOBcI',
                    'homepage': 'http://www.disneyplus.com/series/the-mandalorian/3jLIGMDYINqD',
                    'status': 'returning series',
                    'rating': 8.453589800939387,
                    'votes': 22355,
                    'comment_count': 105,
                    'aired_episodes': 24
                  }])
    
    input_details, input_genres = api.process_recommended_shows(input)

    # if (input_details == expected).all().all():
    #     print("DataFrames are equal")
    # else:
    #     print("DataFrames are not equal")
    #     # Handle the inequality here, if needed
    # try:
    #     assert input_details.equals(expected), "Show detail dataframes equal each other"
    #     print("DataFrames are equal")
    # except AssertionError:
    #     print("DataFrames are not equal")
    assert input_details.equals(expected_details), "Show details dataframes do not equal each other"
    assert input_genres.equals(expected_genres), "Genre details dataframes do not equal each other"
