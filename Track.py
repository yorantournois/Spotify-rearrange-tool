
class Track:

    def __init__(self, name, id, artists, key, mode, energy, valence):

        self.name = name
        self.id = id
        self.artists = [x['name'] for x in artists]
        self.key = key
        self.mode = mode
        self.energy = energy
        self.valence = valence

    def distance_to(self, ref_name, ref_artists, ref_key, ref_mode, ref_energy, ref_valence):

        weights = {'key': 10, 'mode': 4, 'valence': 1, 'energy': 1}
        if self.name == ref_name and any(artist in self.artists for artist in ref_artists):
            return 0

        elif self.key == -1 or ref_key == -1:
            return -1

        else:

            key_distance = min([abs(self.key - x)
                                for x in [ref_key, ref_key + 12, ref_key - 12]])
            mode_distance = abs(self.mode - ref_mode)
            energy_distance = abs(self.energy - ref_energy)
            valence_distance = abs(self.valence - ref_valence)

            distance = weights['key'] * key_distance + weights['mode'] * mode_distance + weights[
                'valence'] * valence_distance + weights['energy'] * energy_distance
            return distance

    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"

    def __str__(self):
        return f'{self.name} - {" ,".join(artist for artist in self.artists)}'