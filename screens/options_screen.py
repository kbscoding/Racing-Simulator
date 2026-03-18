import pygame
from screens.base_screen import BaseScreen
from utils.helpers import scaled, pct_to_rect

BACK_BUTTON = (0.875, 0.090, 0.08, 0.06)
OPTIONS_IMG = "Images/options.png"

class OptionsScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.bg = pygame.image.load(OPTIONS_IMG)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if pct_to_rect(BACK_BUTTON, self.game.current_size).collidepoint(mx, my):
                from screens.main_menu import MainMenuScreen
                self.game.change_screen(MainMenuScreen(self.game))

    def draw(self, surface):
        surface.blit(scaled(self.bg, self.game.current_size), (0, 0))
