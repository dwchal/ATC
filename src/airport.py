import numpy as np

class Airport:
    def __init__(self, name, icao, lat, lon):
        self.name = name
        self.icao = icao
        self.lat = lat
        self.lon = lon
        self.runways = []
        self.taxiways = []

    def add_runway(self, name, start_pos, end_pos, width):
        self.runways.append({
            'name': name,
            'start_pos': np.array(start_pos, dtype=float),
            'end_pos': np.array(end_pos, dtype=float),
            'width': width
        })

    def add_taxiway(self, path):
        self.taxiways.append(np.array(path, dtype=float))
