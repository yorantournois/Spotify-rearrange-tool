import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from input import get_playlists

auth_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)
username, playlists = get_playlists(spotify)

for p in playlists:

    playlist = p.rearrange()
    playlist.write(username)

exit()
