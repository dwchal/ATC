# Air Traffic Control Simulator

A highly technical air traffic control simulation game focusing on realistic aircraft behavior, navigation, and air traffic management.

## Features

- Real-world physics-based aircraft movement
- Complex navigation system using waypoints and flight paths
- Realistic weather conditions affecting flight patterns
- Multiple aircraft types with different performance characteristics
- Emergency scenario handling
- Separation rules enforcement
- Communication system between ATC and aircraft

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python src/main.py
```

## Game Controls

- Mouse: Select aircraft and waypoints
- Left Click: Issue commands to selected aircraft
- Right Click: Open context menu for additional options
- Space: Pause/Resume simulation
- +/-: Adjust simulation speed
- ESC: Open menu

## Technical Details

The simulation implements:
- ICAO separation standards
- Realistic aircraft performance models
- Standard Terminal Arrival Routes (STARs)
- Standard Instrument Departure Procedures (SIDs)
- Weather effects on aircraft performance
- Conflict detection and resolution 