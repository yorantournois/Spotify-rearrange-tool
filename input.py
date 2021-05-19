from Playlist import Playlist
from Track import Track

CHUNK_SIZE = 100


def get_playlists(spotify):
    username = input('Enter username: ')

    entered_playlists = None
    user_playlists = spotify.user_playlists(username)

    while not entered_playlists:
        entered_playlists = input(
            f"""\nEnter playlists to rearrange or enter 'list-all' to list all of your playlists:""")

        if entered_playlists == 'list-all':

            print(f'Showing playlists for {username}:')
            for i, p in enumerate(user_playlists['items']):
                print(p['name'])

        else:
            entered_playlists = [s.strip() for s in entered_playlists.split(',')]
            playlists = []

            playlists = [Playlist(p['id'], p['name'], []) for p in user_playlists['items'] if
                         p['name'] in entered_playlists]

    playlists = append_track_data(username, playlists, spotify)
    return username, playlists


def append_track_data(username, playlists, spotify):
    for p in playlists:
        tracks = []

        results = spotify.user_playlist_tracks(username, p.id)
        track_data = results['items']
        while results['next']:
            results = spotify.next(results)
            track_data.extend(results['items'])

        track_info = [(t['track']['id'], t['track']['name'], t['track']['artists'], t['track']['popularity']) for t in
                      track_data]
        track_ids = [x[0] for x in track_info]

        chunks = [track_ids[i:i + CHUNK_SIZE] for i in range(0, len(track_ids), CHUNK_SIZE)]

        track_features = []
        for chunk in chunks:
            track_features.extend(
                [(t['key'], t['mode'], t['valence'], t['energy']) for t in spotify.audio_features(chunk)])

        for track_info, track_features in zip(track_info, track_features):
            id, name, artists, popularity = track_info
            key, mode, valence, energy = track_features
            tracks.append(Track(name, id, artists, key, mode, energy, valence))
        p.tracks = tracks

    return playlists
