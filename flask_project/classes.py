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

    def create_playlist(self, client_id, client_secret):
        artist_playlist = Playlist('artist', client_id, client_secret)
        self.artist_playlist_id = artist_playlist.create(self.users)
        
        genre_playlist = Playlist('genre', client_id, client_secret)
        self.genre_playlist_id = genre_playlist.create(self.users)

    def create_infographic(self):
        #def __init__(self, users, num_users):
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
    def __init__(self, type, client_id, client_secret):
        self.type = type
        self.user_id = ''
        self.anonymous_username = 'qidav5qss11ylrmpnuumlactw'
        self.anonymous_client_id = client_id
        self.anonymous_client_secret = client_secret
        self.redirect_uri = 'http://localhost:9000'
        self.scope = 'user-read-recently-played user-modify-playback-state playlist-modify-public'
    
    def create(self, users):
        songs = []
        auth_manager=SpotifyOAuth(client_id=self.anonymous_client_id,client_secret=self.anonymous_client_secret,
                          redirect_uri=self.redirect_uri, scope=self.scope)

        #token = util.prompt_for_user_token(self.anonymous_username, self.scope, client_id=self.anonymous_client_id, client_secret=self.anonymous_client_secret, redirect_uri=self.redirect_uri)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        if self.type == 'artist':
            songs = self.create_by_artist(users,sp)
        elif self.type == 'genre':
            songs = self.create_by_genre(users,sp)
        else:
            print('invalid type')
            return

        generated_playlist_id = sp.user_playlist_create(user = self.anonymous_username, name = 'SPP Generated Playlist', public = True, collaborative=False, description='SPP Generated Playlist')['id']
        sp.user_playlist_add_tracks(user = self.anonymous_client_id, tracks = songs, playlist_id = generated_playlist_id)

        return generated_playlist_id

    def create_by_artist(self, users, sp):

        # auth_manager=SpotifyOAuth(client_id=self.anonymous_client_id,client_secret=self.anonymous_client_secret,
        #                   redirect_uri=self.redirect_uri, scope=self.scope)

        # sp = spotipy.Spotify(auth_manager=auth_manager)

        # auth_manager.cache_handler.save_token_to_cache(
        #             auth_manager.get_access_token(as_dict=False, check_cache=False))

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
        #print('most freq artist:')
        #print(most_frequent_artist)
        #Create and print generated playlist array of songIDs
        for i in range(len(most_frequent_artist)):
            artistTracks = sp.artist_top_tracks(most_frequent_artist[i][1])
            #print(artistTracks)
            for j in range(len(artistTracks['tracks'])):
                generatedPlaylist.append(artistTracks['tracks'][j]['id'])
        #Print
        
        #print(generatedPlaylist)
        #Assign playlist songs value to generated playlist
        return generatedPlaylist[:20]

    def create_by_genre(self, users, sp):

        # auth_manager=SpotifyOAuth(client_id=self.anonymous_client_id,client_secret=self.anonymous_client_secret,
        #                   redirect_uri=self.redirect_uri, scope=self.scope)

        # sp = spotipy.Spotify(auth_manager=auth_manager)

        # auth_manager.cache_handler.save_token_to_cache(
        #             auth_manager.get_access_token(as_dict=False, check_cache=False))

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
        #print('most freq genre')
        #print(most_frequent_genre)
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

        
        #new_genre_list = [genre for genre in genre_list if genre in available_genres][:5]
        #print(new_genre_list)
        #Get 20 recommendations for genres and input into generated playlist
        data = sp.recommendations(seed_genres = list(set(new_genre_list))[:5], limit = 20)
        #print('datae')
        #print(data)
        generatedPlaylist = []
        for i in range(len(data['tracks'])):
            generatedPlaylist.append(data['tracks'][i]['id'])
        #print('gen playlist')
        #print(generatedPlaylist)
        return generatedPlaylist

class Infographic:
    def __init__(self, users, num_users):
        self.users = users #array of users
        self.num_users = num_users

    def create(self):
        # if self.num_users > 2:
        #     self.create_large()
        # else:
        #     self.create_small()
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



    # def create_small(self):
    #     #TODO

    #     pass
