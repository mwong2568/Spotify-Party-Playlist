from flask import Flask, render_template, url_for, redirect, request
from classes import User, Room, Infographic, Playlist, Song
#import spotipy
#from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

test_arr = [1,2,3,5,4]

test_user = User('miles', 1)
data = [test_user]

rooms = []

@app.route('/test', methods=['GET','POST'])
def test():
    
    return render_template('test.html', arr = test_arr, arr2=data)

@app.route('/login', methods=['GET','POST'])
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

    if room_id not in [r.get_room_id() for r in rooms]:
        room = Room(room_id)
    else:
        room = [r for r in rooms if r.get_room_id() == room_id]

    rooms.append(room)

    print([r.get_room_id() for r in rooms])

    return render_template('room.html')
    
@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

@app.route('/infographic')
def infographic():
    return render_template('infographic.html')