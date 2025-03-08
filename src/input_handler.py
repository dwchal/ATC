import pygame
import numpy as np
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, INFO_PANEL_WIDTH,
    BASE_SCALE_FACTOR, RADAR_RANGE,
    SPAWN_BUTTON_WIDTH, SPAWN_BUTTON_HEIGHT, SPAWN_BUTTON_MARGIN,
    MIN_SCALE_FACTOR, MAX_SCALE_FACTOR, ZOOM_STEP,
    AIRCRAFT_CLICK_RADIUS
)

class InputHandler:
    def __init__(self):
        self.dragging = False
        self.drag_start = None
        self.radar_center = np.array([WINDOW_WIDTH - INFO_PANEL_WIDTH, WINDOW_HEIGHT]) // 2
        self.spawn_button_rect = pygame.Rect(
            WINDOW_WIDTH - INFO_PANEL_WIDTH + SPAWN_BUTTON_MARGIN,
            WINDOW_HEIGHT - SPAWN_BUTTON_HEIGHT - SPAWN_BUTTON_MARGIN,
            SPAWN_BUTTON_WIDTH,
            SPAWN_BUTTON_HEIGHT
        )
        self.active_command = None

    def handle_event(self, event, game_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.spawn_button_rect.collidepoint(event.pos):
                    game_state._spawn_aircraft()
                else:
                    # Check for command button clicks first
                    cmd_clicked = self._handle_command_click(event.pos, game_state)
                    if not cmd_clicked:
                        self._handle_left_click(event.pos, game_state)
            elif event.button == 4:  # Mouse wheel up
                self._handle_zoom(game_state.renderer, 'in')
            elif event.button == 5:  # Mouse wheel down
                self._handle_zoom(game_state.renderer, 'out')
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                self.drag_start = None
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.drag_start:
                self._handle_drag(event.pos, game_state)
        
        elif event.type == pygame.KEYDOWN:
            if self.active_command:
                self._handle_command_input(event, game_state)

    def _handle_command_click(self, pos, game_state):
        if not game_state.selected_aircraft:
            return False
            
        aircraft = game_state.aircraft[game_state.selected_aircraft]
        
        # Check each command button
        for cmd_id, button in game_state.renderer.command_buttons.items():
            if button['rect'].collidepoint(pos):
                self._execute_command(cmd_id, aircraft, game_state)
                return True
        
        return False

    def _execute_command(self, cmd_id, aircraft, game_state):
        if cmd_id == 'approach':
            aircraft.cleared_for_approach = not aircraft.cleared_for_approach
        elif cmd_id == 'hold':
            aircraft.holding_pattern = not aircraft.holding_pattern
        elif cmd_id == 'heading':
            # Activate heading input mode
            self.active_command = 'heading'
            game_state.renderer.command_buttons['heading']['active'] = True
        elif cmd_id == 'altitude':
            # Activate altitude input mode
            self.active_command = 'altitude'
            game_state.renderer.command_buttons['altitude']['active'] = True
        elif cmd_id == 'speed':
            # Activate speed input mode
            self.active_command = 'speed'
            game_state.renderer.command_buttons['speed']['active'] = True
        elif cmd_id == 'direct':
            # Activate direct-to mode
            self.active_command = 'direct'
            game_state.renderer.command_buttons['direct']['active'] = True
        elif cmd_id == 'emergency':
            # Toggle emergency status
            pass  # TODO: Implement emergency handling

    def _handle_command_input(self, event, game_state):
        if not game_state.selected_aircraft:
            self._clear_active_command(game_state)
            return
            
        aircraft = game_state.aircraft[game_state.selected_aircraft]
        
        if event.key == pygame.K_RETURN:
            self._clear_active_command(game_state)
        elif event.key == pygame.K_ESCAPE:
            self._clear_active_command(game_state)
        elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
            pass  # Handle deletion if needed
        elif event.unicode.isnumeric():
            value = int(event.unicode)
            if self.active_command == 'heading':
                # Build heading (0-360)
                new_heading = value * 10  # Each digit rotates by 10 degrees
                aircraft.set_target_heading(new_heading % 360)
            elif self.active_command == 'altitude':
                # Build altitude (in hundreds of feet)
                new_altitude = value * 1000  # Each digit is 1000 feet
                aircraft.set_target_altitude(new_altitude)
            elif self.active_command == 'speed':
                # Build speed
                new_speed = value * 10  # Each digit is 10 knots
                aircraft.set_target_speed(new_speed)

    def _clear_active_command(self, game_state):
        if self.active_command:
            game_state.renderer.command_buttons[self.active_command]['active'] = False
            self.active_command = None

    def _handle_zoom(self, renderer, direction):
        if direction == 'in':
            renderer.scale_factor = min(
                renderer.scale_factor + ZOOM_STEP,
                BASE_SCALE_FACTOR * MAX_SCALE_FACTOR
            )
        else:
            renderer.scale_factor = max(
                renderer.scale_factor - ZOOM_STEP,
                BASE_SCALE_FACTOR * MIN_SCALE_FACTOR
            )

    def _handle_left_click(self, pos, game_state):
        # Convert screen position to world coordinates
        world_pos = self._screen_to_world(pos, game_state.renderer.scale_factor)
        
        # Check if click is within radar range
        if np.linalg.norm(world_pos) <= RADAR_RANGE:
            # Try to select an aircraft
            selected = False
            for callsign, aircraft in game_state.aircraft.items():
                if np.linalg.norm(aircraft.position - world_pos) < AIRCRAFT_CLICK_RADIUS:
                    game_state.select_aircraft(callsign)
                    selected = True
                    break
            
            if not selected:
                game_state.selected_aircraft = None
            
            # If an aircraft is selected and in heading mode, set new heading
            if self.active_command == 'heading' and game_state.selected_aircraft:
                aircraft = game_state.aircraft[game_state.selected_aircraft]
                delta = world_pos - aircraft.position
                new_heading = np.degrees(np.arctan2(delta[0], delta[1])) % 360
                aircraft.set_target_heading(new_heading)
                self._clear_active_command(game_state)

    def _handle_drag(self, pos, game_state):
        if game_state.selected_aircraft:
            aircraft = game_state.aircraft[game_state.selected_aircraft]
            world_pos = self._screen_to_world(pos, game_state.renderer.scale_factor)
            
            # Calculate new altitude based on vertical drag
            altitude_change = (self.drag_start[1] - pos[1]) * 100  # 100 feet per pixel
            new_altitude = aircraft.altitude + altitude_change
            aircraft.set_target_altitude(new_altitude)
            
            self.drag_start = pos

    def _screen_to_world(self, screen_pos, scale_factor):
        return (np.array(screen_pos) - self.radar_center) / scale_factor 