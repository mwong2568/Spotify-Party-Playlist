from flask import Flask
app = Flask(__name__)


@app.route('/login')
def login():
    return '<h1>Login</h1>'

@app.route('/authorize')
def authorize():
    return '<h1>Spotify authorize access page!</h1>'

@app.route('/home')
def home():
    return '<h1>Home</h1>'

@app.route('/room')
def room():
    return '<h1>Room</h1>'

@app.route('/playlist')
def playlist():
    return '<h1>New Generated Playlist</h1>'

@app.route('/infographic')
def infographic():
    return '<h1>Infographic!!!!!</h1>'