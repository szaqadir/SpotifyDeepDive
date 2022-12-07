import math
from bottle import route, run, request
import spotipy
from spotipy import oauth2
import matplotlib.pyplot as plt
from collections import ChainMap
import mplcursors
import numpy as np
from chord import Chord
import pandas as pd
from collections import Counter
import circlify
import seaborn as sns
import sys

#   To avoid plt.legend() warnings
import logging

logging.getLogger().setLevel(logging.CRITICAL)

mode = sys.argv[1]

if mode == "M":
    CACHE = '.cache'
else:
    CACHE = '.spotipyoauthcache'

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'e43d44dd0cc34a91a559ba1c872bb2b8'
SPOTIPY_CLIENT_SECRET = '0c5e0e4c133d4f3889b97a996ae5e2e2'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-top-read'
# CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,
                               cache_path=CACHE)

access_token = ""

token_info = sp_oauth.get_cached_token()

if token_info:
    # print("Found cached token!")
    access_token = token_info['access_token']
else:
    url = request.url
    code = sp_oauth.parse_response_code(url)
    if code != url:
        # print("Found Spotify auth code in Request URL! Trying to get valid access token...")
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']

if access_token:
    # print("Access token available! Trying to get user information...")
    sp = spotipy.Spotify(access_token)

    ################ CODE HERE ##################
    track_name = []
    release_date = []
    artist_name = []
    track_id = []
    num_songs = 20
    songs = sp.current_user_top_tracks(limit=50, time_range='long_term')

    for i, item in enumerate(songs['items']):
        track_name.append(item['name'])
        s = item['album']['release_date']
        release_date.append(int(s[0:4]))
        artist_name.append(item['artists'][0]['name'])
        track_id.append(item['id'])
    # loading lists into the dataframe

    df = pd.DataFrame({'track_name': track_name, 'release_date': release_date, 'artist_name': artist_name})
    md = df.groupby('release_date').count().to_dict(orient='dict')['track_name']
    md2 = df.groupby('release_date').agg(lambda x: list(x)).to_dict(orient='dict')['track_name']

    genre_list = []
    for artists in artist_name:
        result = sp.search(artists)
        track = result['tracks']['items'][0]

        artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
        genre_list.extend(artist["genres"])

    s = pd.Series(Counter(genre_list), name='genre_val')
    s.index.name = 'genre'
    s = s.reset_index()
    s = s.sort_values('genre_val', ascending=False)
    s = s.head(num_songs)
    s = s.sort_values('genre_val', ascending=True)

    # print(s)
    circles = circlify.circlify(
        s['genre_val'].tolist(),
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1))

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.set_title('Your Top Genres')

    ax.axis('off')

    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    iter = num_songs

    palettes = list(reversed(sns.color_palette("Spectral_r", iter).as_hex()))
    # print(palette)
    # print circles
    labels = s['genre']
    # print(labels)
    for circle, label, palette in zip(circles, labels, palettes):
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r, alpha=0.4, linewidth=2, facecolor=palette))
        plt.annotate(
            label,
            (x, y),
            va='center',
            ha='center'
        )
    plt.show()
# @route('/')
# def index():
#     access_token = ""
#
#     token_info = sp_oauth.get_cached_token()
#
#     if token_info:
#         print("Found cached token!")
#         access_token = token_info['access_token']
#     else:
#         url = request.url
#         code = sp_oauth.parse_response_code(url)
#         if code != url:
#             print("Found Spotify auth code in Request URL! Trying to get valid access token...")
#             token_info = sp_oauth.get_access_token(code)
#             access_token = token_info['access_token']
#
#     if access_token:
#         print("Access token available! Trying to get user information...")
#         sp = spotipy.Spotify(access_token)
#         import pandas as pd
#         ################ CODE HERE ##################
#         track_name = []
#         release_date = []
#         artist_name = []
#         track_id = []
#         num_songs = 20
#         songs = sp.current_user_top_tracks(limit=50, time_range='long_term')
#
#         for i, item in enumerate(songs['items']):
#             track_name.append(item['name'])
#             s = item['album']['release_date']
#             release_date.append(int(s[0:4]))
#             artist_name.append(item['artists'][0]['name'])
#             track_id.append(item['id'])
#         # loading lists into the dataframe
#
#         df = pd.DataFrame({'track_name': track_name, 'release_date': release_date, 'artist_name': artist_name})
#         md = df.groupby('release_date').count().to_dict(orient='dict')['track_name']
#         md2 = df.groupby('release_date').agg(lambda x: list(x)).to_dict(orient='dict')['track_name']
#
#         genre_list = []
#         for artists in artist_name:
#             result = sp.search(artists)
#             track = result['tracks']['items'][0]
#
#             artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
#             genre_list.extend(artist["genres"])
#
#         s = pd.Series(Counter(genre_list), name='genre_val')
#         s.index.name = 'genre'
#         s = s.reset_index()
#         s = s.sort_values('genre_val', ascending=False)
#         s = s.head(num_songs)
#         s = s.sort_values('genre_val', ascending=True)
#
#         # print(s)
#         circles = circlify.circlify(
#             s['genre_val'].tolist(),
#             show_enclosure=False,
#             target_enclosure=circlify.Circle(x=0, y=0, r=1))
#
#         fig, ax = plt.subplots(figsize=(10, 10))
#
#         ax.set_title('Your Top Genres')
#
#         ax.axis('off')
#
#         lim = max(
#             max(
#                 abs(circle.x) + circle.r,
#                 abs(circle.y) + circle.r,
#             )
#             for circle in circles
#         )
#         plt.xlim(-lim, lim)
#         plt.ylim(-lim, lim)
#         iter = num_songs
#
#         palettes = list(reversed(sns.color_palette("Spectral_r", iter).as_hex()))
#         # print(palette)
#         # print circles
#         labels = s['genre']
#         # print(labels)
#         for circle, label, palette in zip(circles, labels, palettes):
#             x, y, r = circle
#             ax.add_patch(plt.Circle((x, y), r, alpha=0.4, linewidth=2, facecolor=palette))
#             plt.annotate(
#                 label,
#                 (x, y),
#                 va='center',
#                 ha='center'
#             )
#         plt.show()
#
#     else:
#         return htmlForLoginButton()
#
#
# def htmlForLoginButton():
#     auth_url = getSPOauthURI()
#     htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
#     return htmlLoginButton
#
#
# def getSPOauthURI():
#     auth_url = sp_oauth.get_authorize_url()
#     return auth_url
#
#
# run(host='', port=8080)
