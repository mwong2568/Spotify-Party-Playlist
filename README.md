# Spotify Party Playlist
Webapp that allows groups of users to generate different playlists that suits the group's preferences <br /> 
<br /> 
## Installation <br /> 
Check requirements.txt for more info <br /> 
 <br /> 
Flask <br /> 
Spotipy <br /> 
Redis <br /> 
Requests <br /> 
Flask-Sessions <br /> 

## Usage

After downloading and unzipping the folder, navigate to the flask_project directory with the terminal.  <br /> 
From there, run the commands: <br /> 
 <br /> 
(for terminal) <br /> 
      $env:FLASK_APP = 'party-playlist.py' <br /> 
      $env:FLASK_DEBUG = 1 <br /> 
(for bash, unverified) <br /> 
      export FLASK_APP = party-playlist.py <br /> 
      export FLASK_DEBUG = 1 <br /> 
 <br /> 
Then run the commmand: <br /> 
      python -m flask run <br /> 
       <br /> 
After this, click on the resulting IPv4 output to access the webpage. <br /> 
Starting up the server may take upwards of a minute. We are simply preprocessing data at this point. <br /> 
From here, follow the instructions on the home page to set up a spotify developer account to retrieve your ClientID and Client Secret, and set the URI. <br /> 
We have created a test room with test user for demo purposes. Please join the room 'demo room' once prompted! <br /> 
Joining a room may also take upwards of a minute! <br /> 
