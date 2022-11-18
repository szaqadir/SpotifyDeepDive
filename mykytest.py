from bottle import route, run, request
import spotipy
from spotipy import oauth2
import pandas as pd

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
        results = sp.current_user()
        # 6Mz6VaWTFrtta4LSXDog4x?si=9b6af5eee8de405f hisashiburi playlist
        # playlist = sp.user_playlist_tracks('spotify', '6Mz6VaWTFrtta4LSXDog4x?si=9b6af5eee8de405f')
        # print(playlist)
        # songs = playlist['items']
        #
        # df = pd.DataFrame(songs)
        # print(df)
        songs = sp.current_user_top_tracks(limit=50, offset=49, time_range='long_term')
        # for i, item in enumerate(top_songs['items']):
        #     print(i, item['name'], '//', item['artists'][0]['name'])
        # print()
        # appending needed data to separate lists
        track_name = []
        artist_name = []
        track_id = []
        for i, item in enumerate(songs['items']):
            track_name.append(item['name'])
            artist_name.append(item['artists'][0]['name'])
            track_id.append(item['id'])

        # loading lists into the dataframe
        df = pd.DataFrame({'artist_name':artist_name,'track_name':track_name,'track_id':track_id})
        print(df)
        return "hehe"

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
