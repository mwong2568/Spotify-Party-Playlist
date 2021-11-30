from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

class User:
    def __init__(self, user_id, user_secret, user_name, userHistory):
        #   authentication
        self.user_id = user_id
        self.user_secret = user_secret
        self.user_name = user_name

        # user data
        self.song_history = []

        songList = []
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=user_id,client_secret=user_secret))

        for i in range(len(userHistory['items'])):
            songId = userHistory['items'][i]['track']['album']['id']
            songArtist = userHistory['items'][i]['track']['album']['artists'][0]['name']
            songArtistId = userHistory['items'][i]['track']['album']['artists'][0]['id']

            result = sp.search(songArtist)
            track=result['tracks']['items'][0]

            artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
            songGenres = artist["genres"]

            self.song_history.append(Song(songId,songArtist,songArtistId,songGenres))



    def whoami(self):
        # test func
        print(self.user_id, self.user_secret, self.user_name)

    def get_song_history(self):
        #TODO: return song hisotry
        #for obj in self.song_history:
        #    print(obj.get_song_id())
        #    print(obj.get_song_artist())
        #    print(obj.get_song_genre())
        pass

    #def createSongList(userHistory):


class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.users = []
        self.artist_playlist_id = ''
        self.genre_playlist_id = ''

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)
        return

    def get_room_id(self):
        return self.room_id

    def get_users(self):
        return self.users

    def create_playlist(self):
        artist_playlist = Playlist('artist')
        self.artist_playlist_id = artist_playlist.create(self.users)
        
        genre_playlist = Playlist('genre')
        self.genre_playlist_id = genre_playlist.create(self.users)

    def create_infographic(self, num_users):
        #TODO
        pass

class Song:
    def __init__(self, song_id, song_artist, song_artist_id, song_genre):
        #variables
        self.song_id = song_id
        self.song_artist = song_artist
        self.song_artist_id = song_artist_id
        self.song_genre = song_genre

    def get_song_id(self):
        return self.song_id

    def get_song_artist(self):
        return self.song_artist

    def get_song_artist_id(self):
        return self.song_artist_id

    def get_song_genre(self):
        return self.song_genre

class Playlist:
    def __init__(self, type):
        self.type = type
        self.anonymous_username = 'milelongpoo'
        self.anonymous_client_id = '1e4ebebf89764ab9889940b50f5de398'
        self.anonymous_client_secret = '1778221d97274a3085d91e2636b686fb'
        self.redirect_uri = 'http://localhost:9000'
        self.scope = 'user-read-recently-played user-modify-playback-state playlist-modify-public'
    
    def create(self, users):
        songs = []
        auth_manager=SpotifyOAuth(client_id=self.anonymous_client_id,client_secret=self.anonymous_client_secret,
                          redirect_uri=self.redirect_uri, scope=self.scope)

        sp = spotipy.Spotify(auth_manager=auth_manager)
        if self.type == 'artist':
            songs = self.create_by_artist(users)
        elif self.type == 'genre':
            songs = self.create_by_genre(users)
        else:
            print('invalid type')
            return

        playlist_id = sp.user_playlist_create(user = self.anonymous_client_id, name = self.anonymous_username, public = True, collaborative=False, description='SPP Generated Playlist')
        sp.user_playlist_add_tracks(user = self.anonymous_client_id, tracks = songs, playlist = playlist_id)

        return playlist_id

    def create_by_artist(self, users):

        auth_manager=SpotifyOAuth(client_id=self.anonymous_client_id,client_secret=self.anonymous_client_secret,
                          redirect_uri=self.redirect_uri, scope=self.scope)

        sp = spotipy.Spotify(auth_manager=auth_manager)

        auth_manager.cache_handler.save_token_to_cache(
                    auth_manager.get_access_token(as_dict=False, check_cache=False))

        #Create array of artistIDs for users in room
        userList=users
        artistIdList = []
        for i in range(len(userList)):
            for j in range(len(userList[i].song_history)):
                artistIdList.append(userList[i].song_history[j].get_song_artist_id())

        #Create hashmap of songs with ids as key and number of duplicates as value
        # for i in range(len(userHistory['items'])):
        #     artistIdList.append(userHistory['items'][i]['track']['album']['artists'][0]['id'])
        generatedPlaylist = []
        artist_counter = defaultdict(int)
        for i in range(len(artistIdList)):
            relatedArtists = sp.artist_related_artists(artistIdList[i])
            for j in range(len(relatedArtists['artists'])):
                artist_counter[relatedArtists['artists'][j]['id']] += 1

        #Create sorted array of 5 most played artists
        most_frequent_artist = sorted([(freq, artist) for artist,
                                    freq in artist_counter.items()], reverse=True)[:5]

        #Create and print generated playlist array of songIDs
        for i in range(len(most_frequent_artist)):
            artistTracks = sp.artist_top_tracks(most_frequent_artist[i][1])
            for j in range(len(artistTracks['tracks'])):
                generatedPlaylist.append(artistTracks['tracks'][j]['album']['id'])
        #Print
        for i in range(len(generatedPlaylist)):
            print(generatedPlaylist[i])
        #Assign playlist songs value to generated playlist
        self.songs = generatedPlaylist

    def create_by_genre(self, users):

        auth_manager=SpotifyOAuth(client_id=self.anonymous_client_id,client_secret=self.anonymous_client_secret,
                          redirect_uri=self.redirect_uri, scope=self.scope)

        sp = spotipy.Spotify(auth_manager=auth_manager)

        auth_manager.cache_handler.save_token_to_cache(
                    auth_manager.get_access_token(as_dict=False, check_cache=False))

        userList=users
        artistGenreList = []
        genre_counter = defaultdict(int)
        for i in range(len(userList)):
            for j in range(len(userList[i].song_history)):
                for genre in userList[i].song_history[j].get_song_genre():
                    genre_counter[genre] += 1

        #Sort hashmap into tuple array
        most_frequent_genre = sorted([(freq, genre) for genre,
                                    freq in genre_counter.items()], reverse=True)[:5]

        #Tuple array into single array of 5 most popular genres
        genre_list = []
        for i in range(len(most_frequent_genre)):
            genre_list.append(most_frequent_genre[i][1])

        #Get 20 recommendations for genres and input into generated playlist
        data = sp.recommendations(seed_genres = genre_list, limit = 20)
        generatedPlaylist = []
        for i in range(len(data['tracks'])):
            generatedPlaylist.append(data['tracks'][i]['id'])

        self.songs = generatedPlaylist

class Infographic:
    def __init__(self, songs, num_users):
        self.songs = songs
        self.num_users = num_users

    def create(self):
        if self.num_users > 2:
            self.create_large()
        else:
            self.create_small()

    def create_large(self):
        #TODO
        pass

    def create_small(self):
        #TODO
        pass
