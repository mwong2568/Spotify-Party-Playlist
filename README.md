# Spotify Party Playlist
Webapp that allows groups of users to generate different playlists that suits the group's preferences <br /> 
<br /> 
## Installation <br /> 
Check requirements.txt for more info <br /> 
 <br /> 
Flask
Spotipy
Redis
Requests
Flask-Sessions

## Usage

After downloading and unzipping the folder, navigate to the flask_project directory with the terminal.
From there, run the commands:
(for terminal)
      $env:FLASK_APP = 'party-playlist.py'
      $env:FLASK_DEBUG = 1
(for bash, unverified)
      export FLASK_APP = party-playlist.py
      export FLASK_DEBUG = 1

Then run the commmand:
      python -m flask run
      
After this, click on the resulting IPv4 output to access the webpage.
From here, follow the instructions on the home page to set up a spotify developer account to retrieve your ClientID and Client Secret, and set the URI.

