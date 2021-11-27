
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#User will enter client id, client secret, and redirect uri
client_id = ''
client_secret = ''
redirect_uri = ''
scope = "user-read-recently-played"

#____Test Variables____
##client_id = 'ee299fd5d24332b15f9d9f5bc18def'
#client_secret = '74aa77871b4b42838130acadeab8ae2c'
#redirect_uri = 'http://localhost:9000'


#Authenticates user with specified ID and allows access to users recently played
auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,
                          redirect_uri=redirect_uri, scope=scope)

sp = spotipy.Spotify(auth_manager=auth_manager)

auth_manager.cache_handler.save_token_to_cache(
            auth_manager.get_access_token(as_dict=False, check_cache=False))

#print(sp.current_user_recently_played(limit=1))
#print(sp.user('4cqen3duqk51gyesbtxvqk9dh'))
