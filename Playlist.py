import spotipy
from operator import itemgetter
from spotipy import SpotifyOAuth


class Playlist:

    def __init__(self, id, name, tracks):

        self.id = id
        self.name = name
        self.tracks = tracks

    def __str__(self):
        return f"Playlist: {self.name}"

    def song_distances(self):
        distances = []
        for i, track in enumerate(self.tracks):
            for ref in self.tracks[i + 1:]:
                distance = track.distance_to(ref.name, ref.artists, ref.key, ref.mode, ref.energy, ref.valence)
                distances.append((distance, track, ref))

        return distances

    def rearrange(self):

        distances = self.song_distances()
        candidates = sorted(distances, key=itemgetter(0), reverse=True)[:10]

        best_total = max(distances)[0] * len(self.tracks)
        best_tracks = self.tracks

        for dist, start, finish in candidates:

            tracks = self.tracks.copy()
            tracks.remove(start)
            tracks.remove(finish)

            temp = start
            new_tracks = [start]
            dists = []

            while tracks:
                valid_pairs = [x for x in distances if temp in x and any([x[1] in tracks, x[2] in tracks])]
                dist, track1, track2 = min(valid_pairs, key=itemgetter(0))
                temp = track1 if track1 != temp else track2

                new_tracks.append(temp)
                dists.append(dist)

                tracks.remove(temp)

            final_dist = temp.distance_to(finish.name, finish.artists, finish.key, finish.mode, finish.energy,
                                          finish.valence)
            new_tracks.append(finish)
            dists.append(final_dist)

            total_dist = sum(dists)

            if total_dist < best_total:
                best_total = total_dist
                best_tracks = new_tracks

        self.name = f'Rearranged | {self.name}'
        self.tracks = best_tracks
        return self

    def write(self, username):

        chunk_size = 100

        token = SpotifyOAuth(scope='playlist-modify-public', username=username)
        spotify = spotipy.Spotify(auth_manager=token)

        rearranged_playlist = spotify.user_playlist_create(user=username, name=self.name, public=True)
        playlist_id = rearranged_playlist['id']
        track_ids = [t.create_spotify_uri() for t in self.tracks]

        chunks = [track_ids[i:i + chunk_size] for i in range(0, len(track_ids), chunk_size)]
        for chunk in chunks:
            spotify.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=chunk)

        return
