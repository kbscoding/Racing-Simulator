import pygame
from screens.base_screen import BaseScreen
from utils.helpers import scaled, pct_to_rect

PLAY_BUTTON = (0.341, 0.400, 0.24, 0.12)
GARAGE_BUTTON = (0.401, 0.630, 0.12, 0.06)
OPTIONS_BUTTON = (0.401, 0.730, 0.12, 0.06)
MAINMENU_IMG = "Images/mainmenu.png"

class MainMenuScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.bg = pygame.image.load(MAINMENU_IMG)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if pct_to_rect(PLAY_BUTTON, self.game.current_size).collidepoint(mx, my):
                from screens.play_screen import PlayScreen
                self.game.change_screen(PlayScreen(self.game))
            elif pct_to_rect(GARAGE_BUTTON, self.game.current_size).collidepoint(mx, my):
                from screens.garage_screen import GarageScreen
                self.game.change_screen(GarageScreen(self.game))
            elif pct_to_rect(OPTIONS_BUTTON, self.game.current_size).collidepoint(mx, my):
                from screens.options_screen import OptionsScreen
                self.game.change_screen(OptionsScreen(self.game))

    def draw(self, surface):
        surface.blit(scaled(self.bg, self.game.current_size), (0, 0))
