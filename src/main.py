import pygame
import sys
from game_state import GameState
from renderer import Renderer
from input_handler import InputHandler
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

class ATCGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Air Traffic Control Simulator")
        self.clock = pygame.time.Clock()
        
        self.renderer = Renderer(self.screen)
        self.game_state = GameState()
        self.game_state.renderer = self.renderer  # Add renderer reference to game state
        self.input_handler = InputHandler()
        
        self.is_running = True
        self.is_paused = False
        self.simulation_speed = 1.0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    self.simulation_speed = min(4.0, self.simulation_speed * 1.5)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.simulation_speed = max(0.25, self.simulation_speed / 1.5)
            
            self.input_handler.handle_event(event, self.game_state)

    def update(self):
        if not self.is_paused:
            self.game_state.update(self.simulation_speed)

    def render(self):
        self.renderer.render(self.game_state)
        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ATCGame()
    game.run() 