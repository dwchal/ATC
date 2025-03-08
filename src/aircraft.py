import math
import numpy as np
from config import (
    CLIMB_RATE, DESCENT_RATE, CRUISE_SPEED,
    MAX_ALTITUDE, MIN_ALTITUDE
)

class Aircraft:
    def __init__(self, callsign, aircraft_type, position, altitude, heading, speed=None):
        self.callsign = callsign
        self.aircraft_type = aircraft_type  # 'small', 'medium', or 'heavy'
        self.position = np.array(position, dtype=float)  # [x, y] in nautical miles
        self.altitude = float(altitude)  # feet
        self.heading = float(heading)  # degrees
        self.speed = float(speed if speed else CRUISE_SPEED[aircraft_type])  # knots
        
        # Flight plan and control
        self.target_altitude = altitude
        self.target_heading = heading
        self.target_speed = self.speed
        self.waypoints = []
        self.cleared_for_approach = False
        self.holding_pattern = False
        
        # Performance characteristics
        self.max_turn_rate = 3.0  # degrees per second
        self.acceleration = 2.0    # knots per second
        self.climb_rate = CLIMB_RATE[aircraft_type]
        self.descent_rate = DESCENT_RATE[aircraft_type]

    def update(self, dt, simulation_speed):
        dt *= simulation_speed
        
        # Update altitude
        if abs(self.target_altitude - self.altitude) > 10:
            if self.target_altitude > self.altitude:
                self.altitude = min(
                    self.altitude + (self.climb_rate * dt / 60),
                    self.target_altitude
                )
            else:
                self.altitude = max(
                    self.altitude - (self.descent_rate * dt / 60),
                    self.target_altitude
                )
        
        # Update speed
        speed_diff = self.target_speed - self.speed
        if abs(speed_diff) > 1:
            self.speed += np.sign(speed_diff) * min(
                abs(speed_diff),
                self.acceleration * dt
            )
        
        # Update heading
        heading_diff = self.get_heading_difference(self.heading, self.target_heading)
        if abs(heading_diff) > 0.5:
            max_turn = self.max_turn_rate * dt
            turn_amount = np.sign(heading_diff) * min(abs(heading_diff), max_turn)
            self.heading = (self.heading + turn_amount) % 360
        
        # Update position based on heading and speed
        heading_rad = math.radians(self.heading)
        velocity = np.array([
            math.sin(heading_rad),
            math.cos(heading_rad)
        ]) * self.speed * dt / 3600  # Convert knots to nm/s
        
        self.position += velocity

    def set_target_altitude(self, altitude):
        self.target_altitude = min(max(altitude, MIN_ALTITUDE), MAX_ALTITUDE)

    def set_target_heading(self, heading):
        self.target_heading = heading % 360

    def set_target_speed(self, speed):
        self.target_speed = min(max(speed, 100), CRUISE_SPEED[self.aircraft_type])

    def add_waypoint(self, waypoint):
        self.waypoints.append(waypoint)

    def clear_waypoints(self):
        self.waypoints = []

    @staticmethod
    def get_heading_difference(current, target):
        diff = target - current
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        return diff

    def get_distance_to(self, other_position):
        return np.linalg.norm(self.position - np.array(other_position))

    def is_in_conflict(self, other_aircraft, horizontal_separation, vertical_separation):
        horizontal_distance = self.get_distance_to(other_aircraft.position)
        vertical_distance = abs(self.altitude - other_aircraft.altitude)
        
        return (horizontal_distance < horizontal_separation and 
                vertical_distance < vertical_separation) 