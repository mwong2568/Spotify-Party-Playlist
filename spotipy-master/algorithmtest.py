import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict

#User will enter client id, client secret, and redirect uri
client_id = ''
client_secret = ''
redirect_uri = ''
scope = 'user-read-recently-played user-modify-playback-state playlist-modify-public'

#____Test Variables____
client_id = 'bfee299fd5d24332b15f9d9f5bc18def'
client_secret = '74aa77871b4b42838130acadeab8ae2c'
redirect_uri = 'http://localhost:9000'


#Authenticates user with specified ID and allows access to users recently played
auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,
                          redirect_uri=redirect_uri, scope=scope)

sp = spotipy.Spotify(auth_manager=auth_manager)

auth_manager.cache_handler.save_token_to_cache(
            auth_manager.get_access_token(as_dict=False, check_cache=False))

userHistory = sp.current_user_recently_played(limit = 5)



result = sp.search('Alaina Castillo')
track=result['tracks']['items'][0]

artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
artistGenreList = artist["genres"]


genre_counter = defaultdict(int)
for i in range(len(artistGenreList)):
    genre_counter[artistGenreList[i]] += 1

most_frequent_genre = sorted([(freq, genre) for genre,
                            freq in genre_counter.items()], reverse=True)[:5]
#print(sp.recommendation_genre_seeds())
genre_list = []
for i in range(len(most_frequent_genre)):
    genre_list.append(most_frequent_genre[i][1])

data = sp.recommendations(seed_genres = genre_list, limit = 20)
generatedPlaylist = []
for i in range(len(data['tracks'])):
    generatedPlaylist.append(data['tracks'][i]['id'])


#print(genre_list)

#print(sp.recommendations(seed_genres = genre_list, limit = 5))



#for x in most_frequent_artist:
 #print(x)

#for i in range(len(most_frequent_artist)):
 #print(most_frequent_artist[i])


#print(sp.current_user())
#data=sp.track('5laBj6BPcK9UlwxzLp2fS4')
#print(data['album']['artists'][0]['name'])
#print(sp.recommendation_genre_seeds())

#data=sp.current_user_recently_played(limit=3)

#for i in range(len(data['items'])):
#    print(data['items'][i]['track']['album']['artists'][0]['name'])

#print(data['items'][0]['track']['album']['artists'][0]['name'])
#print(sp.user('4cqen3duqk51gyesbtxvqk9dh'))
