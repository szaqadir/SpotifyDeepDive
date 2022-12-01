from bottle import route, run, request
import spotipy
from spotipy import oauth2
import matplotlib.pyplot as plt
from collections import ChainMap


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

        track_name = []
        release_date = []
        artist_name = []
        track_id = []
        print(df)
        for i, item in enumerate(songs2['items']):
            track_name.append(item['name'])
            s = item['album']['release_date']
            release_date.append(int(s[0:4]))
            artist_name.append(item['artists'][0]['name'])
            track_id.append(item['id'])
        # loading lists into the dataframe

        df2 = pd.DataFrame({'track_name':track_name, 'release_date':release_date})
        print(df2)

        track_name = []
        release_date = []
        artist_name = []
        track_id = []
        for i, item in enumerate(songs3['items']):
            track_name.append(item['name'])
            s = item['album']['release_date']
            release_date.append(int(s[0:4]))
            artist_name.append(item['artists'][0]['name'])
            track_id.append(item['id'])
        # loading lists into the dataframe

        df3 = pd.DataFrame({'track_name':track_name, 'release_date':release_date})
        print(df3)

        track_name = []
        release_date = []
        artist_name = []
        track_id = []
        for i, item in enumerate(songs4['items']):
            track_name.append(item['name'])
            s = item['album']['release_date']
            release_date.append(int(s[0:4]))
            artist_name.append(item['artists'][0]['name'])
            track_id.append(item['id'])
        # loading lists into the dataframe

        df4 = pd.DataFrame({'track_name':track_name, 'release_date':release_date})
        print(df4)

        frames = [df, df2, df3, df4]

        result = pd.concat(frames)

        md = df.groupby('release_date').count().to_dict(orient='dict')['track_name']
        # print(md)
        dates = list(md.keys())           # list() needed for python 3.x
        numSongs = list(md.values())        # ditto
        plt.plot(dates, numSongs, '-', marker='o') # this will show date at the x-axis
        plt.xlabel("Year of Song Release")
        plt.ylabel("Number of Songs Released")
        # df.plot()
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
