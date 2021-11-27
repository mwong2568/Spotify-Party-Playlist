class User:
    def __init__(self, user_id, user_secret, user_name):
        #   authentication
        self.user_id = user_id
        self.user_secret = user_secret
        self.user_name = user_name

        # user data
        self.song_history = []

    def whoami(self):
        # test func
        print(self.user_id, self.user_secret, self.user_name)

    def get_song_history(self):
        #TODO
        #for obj in self.list:
        #    print(obj.get_song_id())
        pass

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.users = []

    def create_playlist(type):
        #TODO
        pass

    def create_infographic(num_users):
        #TODO
        pass

class Song:
    def __init__(self, song_id):
        #variables
        self.song_id = song_id
        self.song_artist = song_artist
        self.song_genre = song_genre

    def get_song_id(self):
        return self.song_id

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

    def create_by_artist(self):
        #TODO
        pass

    def create_by_genre(self):
        #TODO
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
