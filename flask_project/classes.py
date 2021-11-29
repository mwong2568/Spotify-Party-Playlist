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

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)
        return

    def get_room_id(self):
        return self.room_id

    def get_users(self):
        return self.users

    def create_playlist(self, type):
        #TODO
        pass

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
    def __init__(self, songs, type):
        self.songs = songs
        self.type = type

    def create(self):
        if self.type == 'artist':
            self.create_by_artist()
        elif self.type == 'genre':
            self.create_by_genre()
        else:
            print('invalid type')
            return

    def create_by_artist(self, currentRoom):
        userList=currentRoom.get_users()
        artistIdList = []
        for i in range(len(userList)):
            for j in range(len(userList[i].song_history)):
                artistIdList.append(userList[i].song_history[j].get_song_artist_id())

        #algorithm here

        self.songs =
        pass

    def create_by_genre(self, user.song_history):
        userList=currentRoom.get_users()
        artistGenreList = []
        for i in range(len(userList)):
            for j in range(len(userList[i].song_history)):
                artistGenreList.append(userList[i].song_history[j].get_song_genre())

        #algorithm here
        
        self.songs =
        pass

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
