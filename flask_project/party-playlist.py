from flask import Flask, render_template, url_for, redirect, request, session
from classes import User, Room, Infographic, Playlist, Song
import test_objects
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = 'dfwjhifhaidshjfbgadsikhfbadsihf'
test_arr = [1,2,3,5,4]
test_room = Room('demo room')
test_room.add_user(test_objects.Andrew)
rooms = [test_room]

@app.route('/test', methods=['GET','POST'])
def test():
    
    return render_template('test.html', arr = test_arr)

@app.route('/', methods=['GET','POST'])
def login():
    
    client_id = ''
    client_secret = ''
    redirect_uri = 'http://localhost:9000'
    scope = "user-read-recently-played"

    return render_template('login.html')

@app.route('/spotify')
def spotify():
    return redirect("https://developer.spotify.com/dashboard/")

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if request.method == 'GET':
        return f"The URL is being accessed directly, go back to login"
        
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        client_id = form_data['client_id']
        client_secret = form_data['client_secret']
        name = form_data['name']

        session['client_id'] = client_id
        session['client_secret'] = client_secret
        session['name'] = name

        return render_template('home.html',form_data = form_data)

@app.route('/room', methods = ['POST', 'GET'])
def room():
    if request.method == 'GET':
        room_id = session.get('room_id', None)
        room = [r for r in rooms if r.get_room_id() == room_id][0]
    
    if request.method == 'POST':
        redirect_uri = 'http://localhost:9000'
        scope = "user-read-recently-played"
        client_id = session.get('client_id', None)
        client_secret = session.get('client_secret', None)
        name = session.get('name', None)

        auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,
                          redirect_uri=redirect_uri, scope=scope)
        
        sp = spotipy.Spotify(auth_manager=auth_manager)

        auth_manager.cache_handler.save_token_to_cache(
            auth_manager.get_access_token(as_dict=False, check_cache=False))
        
        recently_played = sp.current_user_recently_played(limit=50)
        print(recently_played)

        room_id = request.form['room_id']

        current_user = User(client_id, client_secret, name, recently_played)

        room = None
        if room_id not in [r.get_room_id() for r in rooms]:
            new_room = Room(room_id)
            rooms.append(new_room)
            room = new_room
        else:
            room = [r for r in rooms if r.get_room_id() == room_id][0]
            
        room.add_user(current_user)
        room.create_playlist(client_id, client_secret)
        room.create_infographic()
        session['room_id'] = room_id
        
    return render_template('room.html')
    
@app.route('/playlist-artist')
def playlist_artist():
    room_id = session.get('room_id', None)
    room = [r for r in rooms if r.get_room_id() == room_id][0]
    playlist_id = room.artist_playlist_id
    link = 'https://open.spotify.com/embed/playlist/' + playlist_id + '?utm_source=generator&theme=0'
    return render_template('playlist-artist.html', link = link)

@app.route('/playlist-genre')
def playlist_genre():
    room_id = session.get('room_id', None)
    room = [r for r in rooms if r.get_room_id() == room_id][0]
    playlist_id = room.genre_playlist_id
    link = 'https://open.spotify.com/embed/playlist/' + playlist_id + '?utm_source=generator&theme=0'
    return render_template('playlist-genre.html', link = link)

@app.route('/infographic')
def infographic():
    room_id = session.get('room_id', None)
    room = [r for r in rooms if r.get_room_id() == room_id][0]

    top_artists, top_genres, top_songs = room.top_artists, room.top_genres, room.top_songs
    users = [user.user_name for user in room.users]

    print(top_artists, top_genres, top_songs)

    return render_template('infographic.html', users = users, top_artists = top_artists, top_genres = top_genres, top_songs = top_songs)