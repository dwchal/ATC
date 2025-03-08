import random
import numpy as np
from aircraft import Aircraft
from config import MIN_SEPARATION_HORIZONTAL, MIN_SEPARATION_VERTICAL, RADAR_RANGE

class GameState:
    def __init__(self):
        self.aircraft = {}  # Dictionary of active aircraft
        self.waypoints = {}  # Dictionary of waypoints
        self.selected_aircraft = None
        self.conflicts = set()  # Set of aircraft pairs in conflict
        self.score = 0
        self.time = 0  # Game time in seconds
        self.weather = self._initialize_weather()
        self.spawn_timer = 0
        self.spawn_interval = 30  # Seconds between aircraft spawns
        
        # Initialize some default waypoints
        self._initialize_waypoints()

    def _initialize_weather(self):
        return {
            'wind_direction': random.uniform(0, 360),
            'wind_speed': random.uniform(0, 30),
            'storms': []  # List of storm centers and radii
        }

    def _initialize_waypoints(self):
        # Add some standard waypoints for the airspace
        standard_waypoints = {
            'NORTH': (0, RADAR_RANGE * 0.8),
            'SOUTH': (0, -RADAR_RANGE * 0.8),
            'EAST': (RADAR_RANGE * 0.8, 0),
            'WEST': (-RADAR_RANGE * 0.8, 0),
            'CENTER': (0, 0)
        }
        
        for name, pos in standard_waypoints.items():
            self.waypoints[name] = {'position': np.array(pos), 'type': 'fix'}

    def update(self, simulation_speed):
        dt = 1.0 / 60.0  # Fixed time step
        self.time += dt * simulation_speed
        
        # Update spawn timer and create new aircraft if needed
        self.spawn_timer += dt * simulation_speed
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self._spawn_aircraft()
        
        # Update aircraft positions
        for aircraft in self.aircraft.values():
            aircraft.update(dt, simulation_speed)
        
        # Check for conflicts
        self.conflicts.clear()
        aircraft_list = list(self.aircraft.values())
        for i in range(len(aircraft_list)):
            for j in range(i + 1, len(aircraft_list)):
                if aircraft_list[i].is_in_conflict(
                    aircraft_list[j],
                    MIN_SEPARATION_HORIZONTAL,
                    MIN_SEPARATION_VERTICAL
                ):
                    self.conflicts.add(
                        tuple(sorted([aircraft_list[i].callsign, aircraft_list[j].callsign]))
                    )
        
        # Update score based on conflicts and successful operations
        self._update_score()
        
        # Remove aircraft that have left the airspace
        self._remove_out_of_range_aircraft()

    def _spawn_aircraft(self):
        # Define spawn points around the radar circle
        spawn_points = [
            ('N', (0, RADAR_RANGE), 180),  # From North, heading South
            ('S', (0, -RADAR_RANGE), 0),   # From South, heading North
            ('E', (RADAR_RANGE, 0), 270),  # From East, heading West
            ('W', (-RADAR_RANGE, 0), 90)   # From West, heading East
        ]
        
        # Randomly select a spawn point
        direction, position, heading = random.choice(spawn_points)
        
        # Generate a unique callsign
        airline_codes = ['AAL', 'UAL', 'DAL', 'SWA', 'JBU']
        flight_number = random.randint(100, 999)
        callsign = f"{random.choice(airline_codes)}{flight_number}"
        
        # Random aircraft type
        aircraft_type = random.choice(['small', 'medium', 'heavy'])
        
        # Random initial altitude between 15000 and 35000 feet
        altitude = random.randint(150, 350) * 100
        
        # Add the new aircraft
        self.add_aircraft(
            callsign=callsign,
            aircraft_type=aircraft_type,
            position=position,
            altitude=altitude,
            heading=heading
        )

    def _update_score(self):
        # Decrease score for each conflict
        self.score -= len(self.conflicts) * 100 * (1.0 / 60.0)  # Points per second
        
        # Increase score for successfully managed aircraft
        for aircraft in self.aircraft.values():
            if aircraft.cleared_for_approach:
                self.score += 1 * (1.0 / 60.0)  # Points per second for good management

    def _remove_out_of_range_aircraft(self):
        to_remove = []
        for callsign, aircraft in self.aircraft.items():
            if np.linalg.norm(aircraft.position) > RADAR_RANGE * 1.2:
                to_remove.append(callsign)
        
        for callsign in to_remove:
            del self.aircraft[callsign]

    def add_aircraft(self, callsign, aircraft_type, position, altitude, heading, speed=None):
        if callsign not in self.aircraft:
            self.aircraft[callsign] = Aircraft(
                callsign, aircraft_type, position, altitude, heading, speed
            )
            return True
        return False

    def remove_aircraft(self, callsign):
        if callsign in self.aircraft:
            del self.aircraft[callsign]
            if self.selected_aircraft == callsign:
                self.selected_aircraft = None
            return True
        return False

    def select_aircraft(self, callsign):
        if callsign in self.aircraft:
            self.selected_aircraft = callsign
            return True
        return False

    def get_selected_aircraft(self):
        if self.selected_aircraft:
            return self.aircraft.get(self.selected_aircraft)
        return None

    def add_waypoint(self, name, position, waypoint_type='fix'):
        if name not in self.waypoints:
            self.waypoints[name] = {
                'position': np.array(position),
                'type': waypoint_type
            }
            return True
        return False

    def get_aircraft_in_range(self, position, range_nm):
        in_range = []
        for aircraft in self.aircraft.values():
            if np.linalg.norm(aircraft.position - np.array(position)) <= range_nm:
                in_range.append(aircraft)
        return in_range 