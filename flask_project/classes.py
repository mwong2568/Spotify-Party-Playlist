class User:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def whoami(self):
        # test func
        print(self.username, self.id)
    
    def get_song_history(self):
        #TODO
        pass

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
    def __init__(self, song_id):
        self.song_id = song_id
    
    def get_artist():
        #TODO 
        pass

    def get_genre():
        #TODO
        pass

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