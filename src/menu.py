import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GREEN, FONT_SIZE

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE + 10)
        self.airports = [("Rochester International (KRST)", "KRST"),
                         ("Minneapolis-St. Paul International (KMSP)", "KMSP"),
                         ("Chicago O'Hare International (KORD)", "KORD")]
        self.selected_airport = None
        self.buttons = self._create_buttons()

    def _create_buttons(self):
        buttons = []
        x = WINDOW_WIDTH // 2 - 150
        y = WINDOW_HEIGHT // 2 - 100
        for name, icao in self.airports:
            rect = pygame.Rect(x, y, 300, 50)
            buttons.append({'rect': rect, 'text': name, 'icao': icao})
            y += 60
        return buttons

    def run(self):
        while self.selected_airport is None:
            self.screen.fill(BLACK)
            self._draw_title()
            self._draw_buttons()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.buttons:
                            if button['rect'].collidepoint(event.pos):
                                self.selected_airport = button['icao']
                                return self.selected_airport

    def _draw_title(self):
        title_text = self.font.render("Select an Airport", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 200))
        self.screen.blit(title_text, title_rect)

    def _draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, GREEN, button['rect'])
            text = self.font.render(button['text'], True, BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
