import math
from bottle import route, run, request
import spotipy
from spotipy import oauth2
import matplotlib.pyplot as plt
from collections import ChainMap
import mplcursors
import numpy as np

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'e43d44dd0cc34a91a559ba1c872bb2b8'
SPOTIPY_CLIENT_SECRET = '0c5e0e4c133d4f3889b97a996ae5e2e2'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-top-read'

CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

@route('/')
def index():

    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code != url:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        import pandas as pd
        ################ CODE HERE ##################
        track_name = []
        release_date = []
        artist_name = []
        track_id = []
        songs = sp.current_user_top_tracks(limit=50,time_range='long_term')
        songs2 = sp.current_user_top_tracks(offset=50, limit=50, time_range='long_term')
        songs3 = sp.current_user_top_tracks(offset=100, limit=50, time_range='long_term')
        songs4 = sp.current_user_top_tracks(offset=150, limit=50, time_range='long_term')
        # song = ChainMap(songs, songs2)
        # song2 = ChainMap(songs3, songs4)
        # finalSong = ChainMap(song, song2)
        # print(finalSong)

        for i, item in enumerate(songs['items']):
            track_name.append(item['name'])
            s = item['album']['release_date']
            release_date.append(int(s[0:4]))
            artist_name.append(item['artists'][0]['name'])
            track_id.append(item['id'])
        # loading lists into the dataframe

        df = pd.DataFrame({'track_name':track_name, 'release_date':release_date})
        md = df.groupby('release_date').count().to_dict(orient='dict')['track_name']
        md2 = df.groupby('release_date').agg(lambda x: list(x)).to_dict(orient='dict')['track_name']
        print(md)
        print(md2)
        

        fig, ax = plt.subplots()
        dates = list(md.keys())           # list() needed for python 3.x
        numSongs = list(md.values())        # ditto
        ax.bar(dates, numSongs, width = 0.3) # this will show date at the x-axis
        ax.set(title="How old is your music taste?", xlabel="Year of Song Release", ylabel="Number of Songs Released")
        cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Transient)
        @cursor.connect("add")
        def on_add(sel):
            x, y, width, height = sel.artist[sel.index].get_bbox().bounds
            x = math.ceil(x)
            print(x)
            z = md2.get(x)
            print(z)
            # print(z)
            sel.annotation.set(text="\n".join(z),
                            position=(0, -20), anncoords="offset points")
            # sel.annotation.xy = (x + width / 2, y + height)

        plt.show()

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='', port=8080)
