from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)


@app.route('/')
def login():
    return render_template('index.html')


@app.route('/authorize')
def authorize():
    return render_template('auth.html')

@app.route('/spotify')
def spotify():
    return redirect("https://developer.spotify.com/")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/room')
def room():
    return '<h1>Room</h1>'

@app.route('/playlist')
def playlist():
    return '<h1>New Generated Playlist</h1>'

@app.route('/infographic')
def infographic():
    return '<h1>Infographic!!!!!</h1>'
