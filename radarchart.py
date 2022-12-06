import numpy as np
import matplotlib.pyplot as plt
import spotipy
from spotipy import oauth2
from bottle import request
import pandas as pd
import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

#   To avoid plt.legend() warnings
import logging

logging.getLogger().setLevel(logging.CRITICAL)

categories = ['Acousticness', 'Danceability', 'Energy', 'Speechiness', 'Valence']
categories = [*categories, categories[0]]

# df0 = pd.read_json('~/Documents/CS 439/Final Project/MyExtData/endsong_0.json')
# df1 = pd.read_json('~/Documents/CS 439/Final Project/MyExtData/endsong_1.json')
# df = pd.concat([df0, df1], axis=0)
# df = df[df.ms_played > 60000]  # user must have listened to at least 1 minute of a song
# df = df[['spotify_track_uri', 'ms_played']]
#
# df = df.groupby('spotify_track_uri').size().to_frame('play_count').reset_index().sort_values('play_count',
#                                                                                              ascending=False).head(5)

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

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE)

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

    songs = sp.current_user_top_tracks(limit=5, time_range='long_term')
    track_name = []
    artist_name = []
    track_id = []
    for i, item in enumerate(songs['items']):
        track_name.append(item['name'])
        artist_name.append(item['artists'][0]['name'])
        track_id.append(item['id'])

    df = pd.DataFrame({'artist_name': artist_name, 'track_name': track_name, 'spotify_track_uri': track_id})
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


# label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(one))
#
# plt.figure(figsize=(8, 8))
# plt.subplot(polar=True)
# plt.plot(label_loc, one, label=title1)
# plt.fill(label_loc, one, alpha=0.2)
#
# plt.plot(label_loc, two, label=title2)
# plt.fill(label_loc, two, alpha=0.2)
#
# plt.plot(label_loc, three, label=title3)
# plt.fill(label_loc, three, alpha=0.2)
#
# plt.plot(label_loc, four, label=title4)
# plt.fill(label_loc, four, alpha=0.2)
#
# plt.plot(label_loc, five, label=title5)
# plt.fill(label_loc, five, alpha=0.2)
#
# plt.title('Top Song Comparison', size=20, y=1.05)
# lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
# plt.legend()
# plt.show()

# Add some text to help the user understand the chart
# For example, tracks with high valence sound more positive (e.g. happy, cheerful, euphoric),
# while tracks with low valence sound more negative (e.g. sadpy, depressed, angry).

# Incorporate recommendations based off of top 5 as well

class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        layout = QVBoxLayout()

        self.one_cb = QCheckBox(title1)
        self.one_cb.setChecked(True)
        self.two_cb = QCheckBox(title2)
        self.three_cb = QCheckBox(title3)
        self.four_cb = QCheckBox(title4)
        self.five_cb = QCheckBox(title5)

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.one_checked = True
        self.two_checked = False
        self.three_checked = False
        self.four_checked = False
        self.five_checked = False

        self.one_cb.stateChanged.connect(self.plot_one)
        self.two_cb.stateChanged.connect(self.plot_two)
        self.three_cb.stateChanged.connect(self.plot_three)
        self.four_cb.stateChanged.connect(self.plot_four)
        self.five_cb.stateChanged.connect(self.plot_five)

        self.plot()

        layout.addWidget(self.toolbar)
        # layout.addWidget(self.canvas)
        sublayout = QVBoxLayout()
        sublayout.addWidget(QLabel("Your Top 5 Songs This Year"))
        sublayout.addWidget(self.one_cb)
        sublayout.addWidget(self.two_cb)
        sublayout.addWidget(self.three_cb)
        sublayout.addWidget(self.four_cb)
        sublayout.addWidget(self.five_cb)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        sublayout.addItem(verticalSpacer)

        grid = QGridLayout()  # 1 x 2
        grid.addLayout(sublayout, 0, 0)
        grid.addWidget(self.canvas, 0, 1)
        layout.addLayout(grid)
        layout.addWidget(QLabel("======================    Key    ======================\n"
                                "Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic\n"
                                "Danceability: How suitable a track is for dancing based on tempo, "
                                "rhythm stability, beat strength, and overall regularity\n"
                                "Energy: A perceptual measure of intensity and activity based on"
                                " dynamic range, perceived loudness, timbre, onset rate, and general entropy\n"
                                "Speechiness: The presence of spoken words in a track\n"
                                "Valence: The musical positiveness conveyed by a track.\n"
                                "==================================================="))
        self.setLayout(layout)

    def plot_one(self, checked):
        if checked:
            self.one_checked = True
        else:
            self.one_checked = False
        self.plot()

    def plot_two(self, checked):
        if checked:
            self.two_checked = True
        else:
            self.two_checked = False
        self.plot()

    def plot_three(self, checked):
        if checked:
            self.three_checked = True
        else:
            self.three_checked = False
        self.plot()

    def plot_four(self, checked):
        if checked:
            self.four_checked = True
        else:
            self.four_checked = False
        self.plot()

    def plot_five(self, checked):
        if checked:
            self.five_checked = True
        else:
            self.five_checked = False
        self.plot()

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111, polar=True)

        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(one))

        if self.one_checked:
            plt.plot(label_loc, one, label=title1)
            plt.fill(label_loc, one, alpha=0.2)
        if self.two_checked:
            plt.plot(label_loc, two, label=title2)
            plt.fill(label_loc, two, alpha=0.2)
        if self.three_checked:
            plt.plot(label_loc, three, label=title3)
            plt.fill(label_loc, three, alpha=0.2)
        if self.four_checked:
            plt.plot(label_loc, four, label=title4)
            plt.fill(label_loc, four, alpha=0.2)
        if self.five_checked:
            plt.plot(label_loc, five, label=title5)
            plt.fill(label_loc, five, alpha=0.2)
        plt.title('Top Song Comparison', size=20, y=1.05)
        lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
        plt.legend()

        self.canvas.draw()


def run():
    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()
    main.resize(900, 900)

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())


# driver code
if __name__ == '__main__':
    run()
    # # creating apyqt5 application
    # app = QApplication(sys.argv)
    #
    # # creating a window object
    # main = Window()
    # main.resize(900, 900)
    #
    # # showing the window
    # main.show()
    #
    # # loop
    # sys.exit(app.exec_())
