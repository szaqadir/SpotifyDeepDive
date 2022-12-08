import spotipy
from spotipy import oauth2
from bottle import request
import pandas as pd
from time import sleep
import os

mode = input("Demo mode (M/S):")
if mode == "M":
    df0 = pd.read_json('MykyData/StreamingHistory0.json')
    df1 = pd.read_json('MykyData/StreamingHistory1.json')
    df_all = pd.concat([df0, df1], axis=0)
    CACHE = '.cache'
else:
    df0 = pd.read_json('SafiData/StreamingHistory0.json')
    df1 = pd.read_json('SafiData/StreamingHistory1.json')
    df2 = pd.read_json('SafiData/StreamingHistory2.json')
    df3 = pd.read_json('SafiData/StreamingHistory3.json')
    df_all = pd.concat([df0, df1, df2, df3], axis=0)
    CACHE = '.spotipyoauthcache'

print("""                                                                                                                  
      .=*+:                                                           
    -=   :##.                   :---:::..                             
    %-    :%-                 -%%########%%##**++==-:.                
    -#*++*#-              :+#%%%+============++**#%%#%%:              
       ..              .=%%***%%%%%%%%%###***++=====*#%+              
   ::*+:             -*%%%#%%%%%#**++++***##%%%%%##++#%%*:            
  **  *#           :#%*%%%%%*+++++++++=------=+*%%%%###*%%*.          
  =#*#*.  =+**  -+#%%%%%%*+*%%%%%%%%%%%%%*+------+#%%%#--%%%:         
         .%+#+:#%%**#%%*=#%%%%%%%%%%%%%%%%%%*------=#%%%#=%%%.        
           : -%%#==+%%++%%%%%%%%%####%%%%%%%%%=------*%%%%%%%#=.      
             %%#==+%%*=%%%%%%*+=======+*%%%%%%%=---=#%%#*+*#*##%*.    
            -%%===%%%-*%%%%#==+*#####+===*%%%%%*--=%%%+=*%#+===+%%.   
            +%#==+%%#-*%%%%%#%%#*++**#%*+*%%%%%%--#%%++%#=======#%+   
            +%#==+%%#-=%%%%%%%+=+++===+%%%%%%%%#-=%%*=##========*%*   
            .%%#==*%%--#%%%%%%%%%##%#*#%%%%%%%%=-+%%*=%+========%%=   
             .#%%##%%*-=#%%%%%%*====#%%%%%%%%%+--+%%*=%*=======#%#    
               :+++#%%*--*%%%%%%%%%#%%%%%%%%#=----#%%+*%+=====#%#.    
                    *%%%+-=*#%%%%%%%%%%%%%*=-------+%%***+++#%%+      
                     :*%%%*=--=+**####*+=----------+#%%%%%%#*=        
                       :+%%%%#*=---------------=+#%%%%=.              
                          :=#%%%%%#****++++**#%%%%#=:                 
                              :=+##%%%%%%%###*+=:                     
                    """)
print("\t\tWelcome to Spotify Deep Dive!")
sleep(1)
print("It's time to take a deep dive into your 2022 listening history!")
input("(Press Enter to continue)")
# print("Click the following link to log into your Spotify account:")

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'e43d44dd0cc34a91a559ba1c872bb2b8'
SPOTIPY_CLIENT_SECRET = '0c5e0e4c133d4f3889b97a996ae5e2e2'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-top-read'
#
sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,
                               cache_path=CACHE)

sp = spotipy.Spotify(auth_manager=sp_oauth)

# df0 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory0.json')
# df1 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory1.json')
# df_all = pd.concat([df0, df1], axis=0)
ms_sum = df_all['msPlayed'].sum()
total_sec = int(ms_sum / 1000)
minutes = int(total_sec / 60)

print("\nThis year, you listened to a grand total of...", minutes, "minutes on Spotify.")
input("(Press Enter to continue)")


print("\nYour top songs this year were...")
sleep(1)
songs = sp.current_user_top_tracks(limit=5, time_range='long_term')
# track_name = []
# artist_name = []
for i, item in enumerate(songs['items']):
    print(i + 1, ")", item['name'], "-", item['artists'][0]['name'])

input("(Press Enter to continue)")


print("\nYour top artists this year were...")
sleep(1)


artists = sp.current_user_top_artists(limit=5, time_range='long_term')
for i, item in enumerate(artists['items']):
    print(i + 1, ")",  item['name'])

input("(Press Enter to continue)")


print("\nWow! What a great year of listening to music.\nLet's take a deeper dive into understanding "
      "what you like and your listening trends...")
input("(Press Enter to continue)")

print("\nIn terms of your top artists, the following visualization shows how much you listen to them and when! "
      "\nFrom this, you can identify listening trends throughout the year.")
sleep(1)
os.system("python stackedArtists.py " + mode)
input("(Press Enter to continue)")

print("\nNext, we will look more into your listening habits."
      "\nWhat days do you like to listen to music the most? What times?")
sleep(1)
os.system("python heatmap.py " + mode)
input("(Press Enter to continue)")

print("\nOver the years, music changes. It reflects the history, culture, and artists of that time period.\n"
      "Does your music taste lie in the past or in the present?")
os.system("python musicage.py " + mode)
sleep(1)

input("(Press Enter to continue)")

print("\nWhile genre is mostly just a label, it is representative of where a song comes from and what it could be"
      " inspired by.\nWhat are the genres that have dominated your year?")
os.system("python genremap.py " + mode)
sleep(1)

input("(Press Enter to continue)")

print("\nLastly, let's analyze your favorite songs! The following visualization will allow you to"
      " see the attributes of your top 5 songs, like"
      "\nacousticness, energy, etc., and compare them against each other."
      " Is there a certain type of music that you like the most?")
sleep(1)
os.system("python radarchart.py " + mode)
input("(Press Enter to continue)")

print("\nA person's music taste is an extension of their personality and reflection of their journey "
      "throughout the year."
      "\nFrom deep diving into your Spotify data, we hope you were able to learn more about yourself.")
input("(Press Enter to continue)")

print("\nTo conclude, here is a list of songs we think you might like based on everything we've compiled!")
sleep(1)
track_id = []
artists = []
for i, item in enumerate(songs['items']):
    track_id.append(item['id'])
    artists.append(item['artists'][0]['name'])
results = sp.recommendations(seed_tracks=track_id)
for track in results['tracks']:
    print('\t', track['name'], '-', track['artists'][0]['name'], '(https://open.spotify.com/track/' + track['id'] + ')')

input("(Press Enter to continue)")
print("\nThank you for using Spotify Deep Dive!")









