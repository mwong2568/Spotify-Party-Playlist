from flask import Flask, render_template, url_for, redirect, request, session
from classes import User, Room, Infographic, Playlist, Song

import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = 'dfwjhifhaidshjfbgadsikhfbadsihf'
test_arr = [1,2,3,5,4]

#test_user = User('miles', 1)
#data = [test_user]

rooms = []

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
        redirect_uri = 'http://localhost:9000'
        scope = "user-read-recently-played"
        auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,
                          redirect_uri=redirect_uri, scope=scope)
        
        sp = spotipy.Spotify(auth_manager=auth_manager)

        auth_manager.cache_handler.save_token_to_cache(
            auth_manager.get_access_token(as_dict=False, check_cache=False))
        
        print(sp.current_user_recently_played(limit=1))

        # Change empty list to function
        session['client_id'] = client_id
        session['client_secret'] = client_secret
        session['name'] = name
        # Create a new User object using form_data info
        return render_template('home.html',form_data = form_data)

@app.route('/room', methods = ['POST', 'GET'])
def room():
    if request.method == 'GET':
        return f"The URL is being accessed directly, go back to login"
    if request.method == 'POST':
        room_id = request.form['room_id']
        print('room')
        #print(form_data)

        #User object should be added to room

    current_user = User(session.get('client_id', None), session.get('client_secret', None), session.get('name', None), [])
    print(current_user.whoami())
    room = None
    if room_id not in [r.get_room_id() for r in rooms]:
        new_room = Room(room_id)
        rooms.append(new_room)
        room = new_room
    else:
        room = [r for r in rooms if r.get_room_id() == room_id]
        
    room.add_user(current_user)
    print([r.get_room_id() for r in rooms])

    for user in room.get_users():
        print(user.whoami())

    return render_template('room.html')
    
@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

@app.route('/infographic')
def infographic():
    return render_template('infographic.html')