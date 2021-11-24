from flask import Flask, render_template
app = Flask(__name__)

test_arr = [1,2,3,5,4]

data = []

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('test.html',arr = test_arr)

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