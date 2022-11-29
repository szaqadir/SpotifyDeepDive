import numpy as np
import matplotlib.pyplot as plt
import spotipy
from spotipy import oauth2
from bottle import request
import pandas as pd

categories = ['Acousticness', 'Danceability', 'Energy', 'Speechiness', 'Valence']
categories = [*categories, categories[0]]

# gather lists for each song! (we going for 5 >:))

df0 = pd.read_json('~/Documents/CS 439/Final Project/MyExtData/endsong_0.json')
df1 = pd.read_json('~/Documents/CS 439/Final Project/MyExtData/endsong_1.json')
df = pd.concat([df0, df1], axis=0)
df = df[df.ms_played > 60000]  # user must have listened to at least 1 minute of a song
df = df[['spotify_track_uri', 'ms_played']]

df = df.groupby('spotify_track_uri').size().to_frame('play_count').reset_index().sort_values('play_count',
                                                                                             ascending=False).head(5)
one = []
two = []
three = []
four = []
five = []

title1 = ""
title2 = ""
title3 = ""
title4 = ""
title5 = ""

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'e43d44dd0cc34a91a559ba1c872bb2b8'
SPOTIPY_CLIENT_SECRET = '0c5e0e4c133d4f3889b97a996ae5e2e2'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-top-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,
                               cache_path=CACHE)

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

    # This is so ugly.. forgive me.
    one.append(sp.audio_features(df.iloc[0]['spotify_track_uri'])[0]['acousticness'])
    one.append(sp.audio_features(df.iloc[0]['spotify_track_uri'])[0]['danceability'])
    one.append(sp.audio_features(df.iloc[0]['spotify_track_uri'])[0]['energy'])
    one.append(sp.audio_features(df.iloc[0]['spotify_track_uri'])[0]['speechiness'])
    one.append(sp.audio_features(df.iloc[0]['spotify_track_uri'])[0]['valence'])
    title1 = sp.track(df.iloc[0]['spotify_track_uri'])['name']

    two.append(sp.audio_features(df.iloc[1]['spotify_track_uri'])[0]['acousticness'])
    two.append(sp.audio_features(df.iloc[1]['spotify_track_uri'])[0]['danceability'])
    two.append(sp.audio_features(df.iloc[1]['spotify_track_uri'])[0]['energy'])
    two.append(sp.audio_features(df.iloc[1]['spotify_track_uri'])[0]['speechiness'])
    two.append(sp.audio_features(df.iloc[1]['spotify_track_uri'])[0]['valence'])
    title2 = sp.track(df.iloc[1]['spotify_track_uri'])['name']

    three.append(sp.audio_features(df.iloc[2]['spotify_track_uri'])[0]['acousticness'])
    three.append(sp.audio_features(df.iloc[2]['spotify_track_uri'])[0]['danceability'])
    three.append(sp.audio_features(df.iloc[2]['spotify_track_uri'])[0]['energy'])
    three.append(sp.audio_features(df.iloc[2]['spotify_track_uri'])[0]['speechiness'])
    three.append(sp.audio_features(df.iloc[2]['spotify_track_uri'])[0]['valence'])
    title3 = sp.track(df.iloc[2]['spotify_track_uri'])['name']

    four.append(sp.audio_features(df.iloc[3]['spotify_track_uri'])[0]['acousticness'])
    four.append(sp.audio_features(df.iloc[3]['spotify_track_uri'])[0]['danceability'])
    four.append(sp.audio_features(df.iloc[3]['spotify_track_uri'])[0]['energy'])
    four.append(sp.audio_features(df.iloc[3]['spotify_track_uri'])[0]['speechiness'])
    four.append(sp.audio_features(df.iloc[3]['spotify_track_uri'])[0]['valence'])
    title4 = sp.track(df.iloc[3]['spotify_track_uri'])['name']

    five.append(sp.audio_features(df.iloc[4]['spotify_track_uri'])[0]['acousticness'])
    five.append(sp.audio_features(df.iloc[4]['spotify_track_uri'])[0]['danceability'])
    five.append(sp.audio_features(df.iloc[4]['spotify_track_uri'])[0]['energy'])
    five.append(sp.audio_features(df.iloc[4]['spotify_track_uri'])[0]['speechiness'])
    five.append(sp.audio_features(df.iloc[4]['spotify_track_uri'])[0]['valence'])
    title5 = sp.track(df.iloc[4]['spotify_track_uri'])['name']

# connecting the shape back to first point
one = [*one, one[0]]
two = [*two, two[0]]
three = [*three, three[0]]
four = [*four, four[0]]
five = [*five, five[0]]

label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(one))

plt.figure(figsize=(8, 8))
plt.subplot(polar=True)
plt.plot(label_loc, one, label=title1)
plt.fill(label_loc, one, alpha=0.2)

plt.plot(label_loc, two, label=title2)
plt.fill(label_loc, two, alpha=0.2)

plt.plot(label_loc, three, label=title3)
plt.fill(label_loc, three, alpha=0.2)

plt.plot(label_loc, four, label=title4)
plt.fill(label_loc, four, alpha=0.2)

plt.plot(label_loc, five, label=title5)
plt.fill(label_loc, five, alpha=0.2)

plt.title('Top Song Comparison', size=20, y=1.05)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
plt.legend()
plt.show()
