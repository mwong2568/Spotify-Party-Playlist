from flask import Flask, render_template
from classes import User, Room, Infographic, Playlist, Song

app = Flask(__name__)

test_arr = [1,2,3,5,4]

test_user = User('miles', 1)
data = [test_user]

@app.route('/test', methods=['GET','POST'])
def test():
    return render_template('test.html', arr = test_arr, arr2=data)

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/authorize')
def authorize():
    return '<h1>Spotify authorize access page!</h1>'

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/room')
def room():
    return render_template('room.html')

@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

@app.route('/infographic')
def infographic():
    return render_template('infographic.html')