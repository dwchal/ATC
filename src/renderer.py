import pygame
import numpy as np
from config import (
    BLACK, WHITE, GREEN, RED, BLUE, GRAY,
    WINDOW_WIDTH, WINDOW_HEIGHT, RADAR_RANGE,
    BASE_SCALE_FACTOR, INFO_PANEL_WIDTH, FONT_SIZE,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_ACTIVE_COLOR,
    SPAWN_BUTTON_WIDTH, SPAWN_BUTTON_HEIGHT, SPAWN_BUTTON_MARGIN,
    CMD_BUTTON_WIDTH, CMD_BUTTON_HEIGHT, CMD_BUTTON_MARGIN, CMD_BUTTON_SPACING,
    AIRCRAFT_SYMBOL_SIZE, AIRCRAFT_DIRECTION_LENGTH
)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.radar_center = np.array([WINDOW_WIDTH - INFO_PANEL_WIDTH, WINDOW_HEIGHT]) // 2
        self.spawn_button_rect = pygame.Rect(
            WINDOW_WIDTH - INFO_PANEL_WIDTH + SPAWN_BUTTON_MARGIN,
            WINDOW_HEIGHT - SPAWN_BUTTON_HEIGHT - SPAWN_BUTTON_MARGIN,
            SPAWN_BUTTON_WIDTH,
            SPAWN_BUTTON_HEIGHT
        )
        self.scale_factor = BASE_SCALE_FACTOR
        self.command_buttons = self._create_command_buttons()
        
    def _create_command_buttons(self):
        buttons = {}
        commands = [
            ("Set Heading", "heading"),
            ("Set Altitude", "altitude"),
            ("Set Speed", "speed"),
            ("Clear Approach", "approach"),
            ("Hold Pattern", "hold"),
            ("Direct To", "direct"),
            ("Emergency", "emergency")
        ]
        
        x = WINDOW_WIDTH - INFO_PANEL_WIDTH + CMD_BUTTON_MARGIN
        y = 300  # Start position after aircraft info
        
        for label, cmd_id in commands:
            rect = pygame.Rect(x, y, CMD_BUTTON_WIDTH, CMD_BUTTON_HEIGHT)
            buttons[cmd_id] = {
                'rect': rect,
                'label': label,
                'active': False
            }
            y += CMD_BUTTON_HEIGHT + CMD_BUTTON_SPACING
        
        return buttons
        
    def render(self, game_state):
        self.screen.fill(BLACK)
        
        # Draw radar circle and range rings
        pygame.draw.circle(self.screen, GRAY, self.radar_center, RADAR_RANGE * self.scale_factor, 1)
        for range_nm in [10, 20, 30, 40]:
            pygame.draw.circle(
                self.screen, GRAY, self.radar_center,
                range_nm * self.scale_factor, 1
            )
        
        # Draw compass points
        self._draw_compass_points()
        
        # Draw airport layout
        self._draw_airport(game_state.active_airport)

        # Draw waypoints
        for name, waypoint in game_state.waypoints.items():
            screen_pos = self._world_to_screen(waypoint['position'])
            pygame.draw.circle(self.screen, BLUE, screen_pos, 5)
            self._draw_text(name, screen_pos + np.array([10, -10]), WHITE)
        
        # Draw aircraft
        for aircraft in game_state.aircraft.values():
            self._draw_aircraft(aircraft, game_state.selected_aircraft == aircraft.callsign)
        
        # Draw conflicts
        for conflict in game_state.conflicts:
            aircraft1 = game_state.aircraft[conflict[0]]
            aircraft2 = game_state.aircraft[conflict[1]]
            pos1 = self._world_to_screen(aircraft1.position)
            pos2 = self._world_to_screen(aircraft2.position)
            pygame.draw.line(self.screen, RED, pos1, pos2, 1)
        
        # Draw information panel
        self._draw_info_panel(game_state)
        
        # Draw spawn button
        self._draw_spawn_button()

    def _world_to_screen(self, position):
        screen_pos = position * self.scale_factor + self.radar_center
        return screen_pos.astype(int)

    def _draw_airport(self, airport):
        # Draw runways
        for runway in airport.runways:
            start_pos = self._world_to_screen(runway['start_pos'])
            end_pos = self._world_to_screen(runway['end_pos'])
            pygame.draw.line(self.screen, GRAY, start_pos, end_pos, int(runway['width'] / 100 * self.scale_factor))

        # Draw taxiways
        for taxiway in airport.taxiways:
            points = [self._world_to_screen(p) for p in taxiway]
            pygame.draw.lines(self.screen, GRAY, False, points, 2)

    def _draw_aircraft(self, aircraft, is_selected):
        screen_pos = self._world_to_screen(aircraft.position)
        
        # Draw aircraft symbol (triangle)
        color = GREEN if is_selected else WHITE
        heading_rad = np.radians(aircraft.heading)
        
        # Calculate triangle points
        direction = np.array([
            np.sin(heading_rad),
            np.cos(heading_rad)
        ])
        right = np.array([
            np.cos(heading_rad),
            -np.sin(heading_rad)
        ])
        
        # Triangle points
        nose = screen_pos + direction * AIRCRAFT_SYMBOL_SIZE
        left_wing = screen_pos - direction * (AIRCRAFT_SYMBOL_SIZE/2) - right * (AIRCRAFT_SYMBOL_SIZE/2)
        right_wing = screen_pos - direction * (AIRCRAFT_SYMBOL_SIZE/2) + right * (AIRCRAFT_SYMBOL_SIZE/2)
        
        # Draw filled triangle for better visibility
        pygame.draw.polygon(self.screen, color, [nose, left_wing, right_wing])
        
        # Draw direction line
        end_pos = screen_pos + direction * AIRCRAFT_DIRECTION_LENGTH
        pygame.draw.line(self.screen, color, screen_pos, end_pos, 2)
        
        # Draw aircraft data block
        label = f"{aircraft.callsign}\n{int(aircraft.altitude/100):03d}\n{int(aircraft.speed)}"
        self._draw_text(label, screen_pos + np.array([15, -20]), color)

    def _draw_compass_points(self):
        compass_points = [
            ('N', (0, -RADAR_RANGE)),
            ('S', (0, RADAR_RANGE)),
            ('E', (RADAR_RANGE, 0)),
            ('W', (-RADAR_RANGE, 0))
        ]
        
        for label, pos in compass_points:
            screen_pos = self._world_to_screen(np.array(pos))
            self._draw_text(label, screen_pos, WHITE)

    def _draw_info_panel(self, game_state):
        panel_rect = pygame.Rect(
            WINDOW_WIDTH - INFO_PANEL_WIDTH, 0,
            INFO_PANEL_WIDTH, WINDOW_HEIGHT
        )
        pygame.draw.rect(self.screen, GRAY, panel_rect, 1)
        
        y = 10
        
        # Draw score
        score_text = f"Score: {int(game_state.score)}"
        self._draw_text(score_text, (panel_rect.x + 10, y), WHITE)
        y += 30
        
        # Draw time
        hours = int(game_state.time // 3600)
        minutes = int((game_state.time % 3600) // 60)
        seconds = int(game_state.time % 60)
        time_text = f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}"
        self._draw_text(time_text, (panel_rect.x + 10, y), WHITE)
        y += 30
        
        # Draw zoom level
        zoom_text = f"Zoom: {self.scale_factor/BASE_SCALE_FACTOR:.1f}x"
        self._draw_text(zoom_text, (panel_rect.x + 10, y), WHITE)
        y += 30
        
        # Draw weather information
        weather_text = [
            f"Wind: {int(game_state.weather['wind_speed'])}kts",
            f"Direction: {int(game_state.weather['wind_direction'])}°"
        ]
        for text in weather_text:
            self._draw_text(text, (panel_rect.x + 10, y), WHITE)
            y += 20
        
        # Draw selected aircraft information
        selected = game_state.get_selected_aircraft()
        if selected:
            y += 20
            info_text = [
                f"Selected: {selected.callsign}",
                f"Type: {selected.aircraft_type}",
                f"Altitude: {int(selected.altitude)}ft",
                f"Speed: {int(selected.speed)}kts",
                f"Heading: {int(selected.heading)}°"
            ]
            for text in info_text:
                self._draw_text(text, (panel_rect.x + 10, y), GREEN)
                y += 20
            
            # Draw command buttons if aircraft is selected
            self._draw_command_buttons(selected)

    def _draw_command_buttons(self, aircraft):
        mouse_pos = pygame.mouse.get_pos()
        
        for cmd_id, button in self.command_buttons.items():
            # Determine button color based on state
            if button['rect'].collidepoint(mouse_pos):
                color = BUTTON_HOVER_COLOR
            elif button['active']:
                color = BUTTON_ACTIVE_COLOR
            else:
                color = BUTTON_COLOR
            
            # Draw button background
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, WHITE, button['rect'], 1)
            
            # Draw button text
            text = self.font.render(button['label'], True, WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
            
            # Add visual indicator for toggleable states
            if cmd_id == 'approach' and aircraft.cleared_for_approach:
                pygame.draw.circle(self.screen, GREEN, 
                    (button['rect'].right - 10, button['rect'].centery), 4)
            elif cmd_id == 'hold' and aircraft.holding_pattern:
                pygame.draw.circle(self.screen, GREEN, 
                    (button['rect'].right - 10, button['rect'].centery), 4)

    def _draw_spawn_button(self):
        # Check if mouse is hovering over button
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER_COLOR if self.spawn_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        
        # Draw button
        pygame.draw.rect(self.screen, color, self.spawn_button_rect)
        pygame.draw.rect(self.screen, WHITE, self.spawn_button_rect, 1)
        
        # Draw button text
        text = self.font.render("Spawn Aircraft", True, WHITE)
        text_rect = text.get_rect(center=self.spawn_button_rect.center)
        self.screen.blit(text, text_rect)

    def _draw_text(self, text, position, color):
        for i, line in enumerate(text.split('\n')):
            text_surface = self.font.render(line, True, color)
            self.screen.blit(
                text_surface,
                (position[0], position[1] + i * (FONT_SIZE + 2))
            ) 