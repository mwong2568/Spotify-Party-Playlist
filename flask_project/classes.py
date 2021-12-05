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
        seen = set()
        for i in range(len(userHistory['items'])):

            songId = userHistory['items'][i]['track']['id']

            songArtist = userHistory['items'][i]['track']['album']['artists'][0]['name']
            songArtistId = userHistory['items'][i]['track']['album']['artists'][0]['id']
            songName = userHistory['items'][i]['track']['name']
            result = sp.search(songArtist)
            track=result['tracks']['items'][0]

            artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
            songGenres = artist["genres"]
            if songId not in seen:
                self.song_history.append(Song(songId,songArtist,songArtistId,songGenres,songName))
                seen.add(songId)

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.users = []
        self.artist_playlist_id = ''
        self.genre_playlist_id = ''
        self.top_artists = []
        self.top_genres = []
        self.top_songs = []

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)
        return

    def get_room_id(self):
        return self.room_id

    def get_users(self):
        return self.users

    def create_playlist(self, client_id, client_secret, username):
        artist_playlist = Playlist('artist', client_id, client_secret, username)
        self.artist_playlist_id = artist_playlist.create(self.users)

        genre_playlist = Playlist('genre', client_id, client_secret, username)
        self.genre_playlist_id = genre_playlist.create(self.users)

    def create_infographic(self):
        infographic_details = Infographic(self.users, len(self.users))
        self.top_artists, self.top_genres, self.top_songs = infographic_details.create()

class Song:
    def __init__(self, song_id, song_artist, song_artist_id, song_genre, song_name):
        #variables
        self.song_id = song_id
        self.song_artist = song_artist
        self.song_artist_id = song_artist_id
        self.song_genre = song_genre
        self.song_name = song_name
    def get_song_id(self):
        return self.song_id

    def get_song_artist(self):
        return self.song_artist

    def get_song_artist_id(self):
        return self.song_artist_id

    def get_song_genre(self):
        return self.song_genre

class Playlist:
    def __init__(self, type, client_id, client_secret, username):
        self.type = type
        self.user_id = ''
        self.anonymous_username = username
        self.anonymous_client_id = client_id
        self.anonymous_client_secret = client_secret
        self.redirect_uri = 'http://localhost:9000'
        self.scope = 'user-read-recently-played user-modify-playback-state playlist-modify-public'

    def create(self, users):
        songs = []
        auth_manager=SpotifyOAuth(client_id=self.anonymous_client_id,
                            client_secret=self.anonymous_client_secret,
                            redirect_uri=self.redirect_uri, scope=self.scope)


        sp = spotipy.Spotify(auth_manager=auth_manager)
        if self.type == 'artist':
            songs = self.create_by_artist(users,sp)
        elif self.type == 'genre':
            songs = self.create_by_genre(users,sp)
        else:
            print('invalid type')
            return

        generated_playlist_id = sp.user_playlist_create(user = self.anonymous_username,
                                name = 'SPP Generated Playlist', public = True, collaborative=False,
                                description='SPP Generated Playlist')['id']
        sp.user_playlist_add_tracks(user = self.anonymous_client_id, tracks = songs, playlist_id = generated_playlist_id)
        return generated_playlist_id

    def create_by_artist(self, users, sp):
        #Create array of artistIDs for users in room
        userList=users
        artistIdList = []
        for i in range(len(userList)):
            for j in range(len(userList[i].song_history)):
                artistIdList.append(userList[i].song_history[j].get_song_artist_id())

        #Create hashmap of songs with ids as key and number of duplicates as value
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
                generatedPlaylist.append(artistTracks['tracks'][j]['id'])

        #Assign playlist songs value to generated playlist
        return generatedPlaylist[:20]

    def create_by_genre(self, users, sp):
        userList=users
        artistGenreList = []
        genre_counter = defaultdict(int)
        for i in range(len(userList)):
            for j in range(len(userList[i].song_history)):
                for genre in userList[i].song_history[j].get_song_genre():
                    genre_counter[genre] += 1

        #Sort hashmap into tuple array
        most_frequent_genre = sorted([(freq, genre) for genre,
                                    freq in genre_counter.items()], reverse=True)

        #Tuple array into single array of 5 most popular genres
        genre_list = []
        for i in range(len(most_frequent_genre)):
            genre_list.append(most_frequent_genre[i][1])

        available_genres=sp.recommendation_genre_seeds()['genres']
        #print(available_genres)
        #print('genrelist')
        #print(genre_list)
        new_genre_list = []

        for genre in genre_list:
            for av_genre in available_genres:
                if av_genre in genre:
                    new_genre_list.append(av_genre)
                    break

        #Get 20 recommendations for genres and input into generated playlist
        data = sp.recommendations(seed_genres = list(set(new_genre_list))[:5], limit = 20)
        generatedPlaylist = []
        for i in range(len(data['tracks'])):
            generatedPlaylist.append(data['tracks'][i]['id'])
        return generatedPlaylist

class Infographic:
    def __init__(self, users, num_users):
        self.users = users #array of users
        self.num_users = num_users

    def create(self):
        return self.create_large()

    def create_large(self):
        userList = self.users

        #Gathering artist ids
        artist_counter = defaultdict(int)
        for i in range(len(userList)):
            for j in range(len(userList[i].song_history)):
                artist_counter[userList[i].song_history[j].get_song_artist()] += 1

        #Create sorted array of 5 most played artists
        most_frequent_artist = sorted([(freq, artist) for artist,
                                    freq in artist_counter.items()], reverse=True)[:5]


        #Gathering genres
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

        songList = []
        song_counter = defaultdict(int)
        for i in range(len(userList)):
            for j in range(len(userList[i].song_history)):
                song_counter[userList[i].song_history[j].song_name] += 1

        most_frequent_song = sorted([(freq, song) for song,
                                freq in song_counter.items()], reverse=True)[:5]

        return most_frequent_artist, most_frequent_genre, most_frequent_song
