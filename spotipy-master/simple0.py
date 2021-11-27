import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = ''
client_secret = ''
redirect_uri = ''

scope = "user-read-recently-played"

auth_manager=SpotifyOAuth(client_id=client_id,
                    client_secret=client_secret, redirect_uri=redirect_uri,
                    scope=scope)

sp = spotipy.Spotify(auth_manager=auth_manager)
auth_manager.cache_handler.save_token_to_cache(auth_manager.get_access_token(check_cache=False))


#auth_manager.refresh_access_token(auth_manager.get_access_token())
#print(auth_manager.get_access_token(as_dict=False))
#print(auth_manager.get_cached_token())
#auth_manager.cache_handler.save_token_to_cache('BQDgFpeybLTAx0m9b2BaKPl80jslI4N6aD0RNb6cf0LaQeyUx8MYZjsS5tKJjHNNqsbDQ5aJ9JTLMq0noev_AgZSRONbp7XwHENcq861CoSVUQt-Cpkino-myksT-TjFHQOS1Z0ApR_2K8sHjMekZY8fdbHw8QLJCN05NoKOHNQf6iB9FnkyRrQUwi2PUtLYLpI')
#print(sp.current_user_recently_played(limit=1))
print(sp.user('4cqen3duqk51gyesbtxvqk9dh'))
#auth_manager.get_auth_response()

#bfee299fd5d24332b15f9d9f5bc18def
#74aa77871b4b42838130acadeab8ae2c

#9dfcbf4ee2644b459915a3351e102e29
#ec591e37666d41d880edc2096716a838
