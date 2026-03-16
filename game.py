import pygame
from screens.main_menu import MainMenuScreen

BASE_W, BASE_H = 1600, 900

class Game:
    def __init__(self):
        pygame.init()

        self.base_size = (BASE_W, BASE_H)
        self.current_size = self.base_size

        self.window = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
        pygame.display.set_caption("Racing Simulator")

        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.SysFont(None, 32)
        self.large_font = pygame.font.SysFont(None, 72)
        self.small_font = pygame.font.SysFont(None, 28)

        # Start with main menu
        self.current_screen = MainMenuScreen(self)

    def change_screen(self, new_screen):
        self.current_screen = new_screen

    def run(self):
        running = True

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.VIDEORESIZE:
                    self.current_size = (event.w, event.h)
                    self.window = pygame.display.set_mode(
                        self.current_size, pygame.RESIZABLE
                    )
                    self.current_screen.on_resize()

                self.current_screen.handle_event(event)

            # Update and draw current screen
            self.current_screen.update()
            self.current_screen.draw(self.window)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
