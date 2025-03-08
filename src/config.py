# Window Settings
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (70, 70, 70)
BUTTON_ACTIVE_COLOR = (0, 100, 0)

# Game Settings
MIN_SEPARATION_HORIZONTAL = 5.0  # Nautical miles
MIN_SEPARATION_VERTICAL = 1000  # Feet
RADAR_RANGE = 50  # Nautical miles
MAX_ALTITUDE = 40000  # Feet
MIN_ALTITUDE = 0  # Feet

# Aircraft Performance
CLIMB_RATE = {
    'small': 2000,    # feet per minute
    'medium': 2500,
    'heavy': 2000
}

DESCENT_RATE = {
    'small': 1500,    # feet per minute
    'medium': 2000,
    'heavy': 1500
}

CRUISE_SPEED = {
    'small': 250,     # knots
    'medium': 350,
    'heavy': 450
}

# Weather Effects
WIND_EFFECT_MULTIPLIER = 0.2
STORM_RADIUS = 10  # Nautical miles

# Waypoint Settings
WAYPOINT_RADIUS = 10
WAYPOINT_COLOR = BLUE

# UI Settings
FONT_SIZE = 14
INFO_PANEL_WIDTH = 300
RADAR_CENTER = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
BASE_SCALE_FACTOR = 2  # base pixels per nautical mile
MIN_SCALE_FACTOR = 1   # minimum zoom level
MAX_SCALE_FACTOR = 4   # maximum zoom level
ZOOM_STEP = 0.25       # zoom increment/decrement
AIRCRAFT_CLICK_RADIUS = 2.0  # nautical miles - increased from 1.0 for easier selection

# Button Settings
SPAWN_BUTTON_WIDTH = 120
SPAWN_BUTTON_HEIGHT = 30
SPAWN_BUTTON_MARGIN = 10

# Command Button Settings
CMD_BUTTON_WIDTH = 140
CMD_BUTTON_HEIGHT = 25
CMD_BUTTON_MARGIN = 5
CMD_BUTTON_SPACING = 5

# Aircraft Display
AIRCRAFT_SYMBOL_SIZE = 15  # pixels
AIRCRAFT_DIRECTION_LENGTH = 20  # pixels 