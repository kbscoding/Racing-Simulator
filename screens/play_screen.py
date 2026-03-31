import pygame
from screens.base_screen import BaseScreen
from cars import Car
from systems.collision_system import CollisionSystem
from utils.helpers import scaled, blur_surface, pct_to_rect

CRASH_THRESHOLD = 50
MASK_SCALE = 0.85
MAINTRACK_IMG = "Images/maintrack2.png"
CAR_IMAGES = [
    "Images/bluef1car.png",
    "Images/whitef1car.png",
    "Images/blueporsche.png",
    "Images/greenporsche.png"
]
START_Y_RATIO = 0.8  # spawn at 80% down the screen

class PlayScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)

        # Track & collision
        self.track = pygame.image.load(MAINTRACK_IMG)
        self.track_surface = None
        self.border_mask = None
        self.border_offset = (0, 0)
        self.collision_system = None
        self.start_line_y = 0

        # Vehicle
        self.vehicle_choice = ""
        self.selected_vehicle = None
        self.car = None

        # Race state
        self.ready_prompt = False
        self.countdown_active = False
        self.countdown_start_ms = 0
        self.race_active = False
        self.race_start_ms = 0
        self.race_end_ms = 0
        self.final_time_ms = None
        self.show_final_time = False
        self.lap_started = False
        self.game_over = False

        # Confirm back overlay
        self.confirm_back = False

        # Initialize track and collision system
        self.prepare_track()

    def prepare_track(self):
        size = self.game.current_size
        scale = size[1] / self.track.get_height()
        new_w = int(self.track.get_width() * scale)

        self.track_surface = pygame.transform.smoothscale(self.track, (new_w, size[1]))
        self.border_mask = pygame.mask.from_surface(self.track_surface)
        self.border_offset = ((size[0] - new_w) // 2, 0)
        self.collision_system = CollisionSystem(self.border_mask, self.border_offset)

        self.start_line_y = int(size[1] * START_Y_RATIO) - 10

    def on_resize(self):
        self.prepare_track()
        if self.selected_vehicle:
            self.spawn_vehicle(self.selected_vehicle)


    def handle_event(self, event):
        # ESC key for back to main menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.confirm_back:
                    from screens.main_menu import MainMenuScreen
                    self.game.change_screen(MainMenuScreen(self.game))
                    self.reset_play_state()
                else:
                    self.confirm_back = True

            # Vehicle selection
            if self.selected_vehicle is None:
                if event.key == pygame.K_RETURN:
                    try:
                        n = int(self.vehicle_choice)
                        if 1 <= n <= 4:
                            self.spawn_vehicle(n)
                    except:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    self.vehicle_choice = self.vehicle_choice[:-1]
                else:
                    ch = event.unicode
                    if ch.isdigit():
                        self.vehicle_choice += ch

        # Mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # READY prompt overlay
            if self.ready_prompt and not self.countdown_active and not self.race_active:
                if event.button == 1:  # left click -> ready
                    self.countdown_active = True
                    self.countdown_start_ms = pygame.time.get_ticks()
                    self.ready_prompt = False
                    self.show_final_time = False
                    self.final_time_ms = None
                    self.lap_started = False
                elif event.button == 3:  # right click -> cancel
                    self.reset_play_state()

            # Cancel confirm back overlay
            if self.confirm_back:
                self.confirm_back = False


    def spawn_vehicle(self, num):
        surf = pygame.image.load(CAR_IMAGES[num-1])
        h = max(24, int(self.game.current_size[1] * 0.05))
        w = int(surf.get_width() * (h / surf.get_height()))
        car_surf = pygame.transform.smoothscale(surf, (w, h))
        self.car = Car(car_surf)
        self.car.x = int(self.game.current_size[0] / 2)
        self.car.y = int(self.game.current_size[1] * START_Y_RATIO)
        self.selected_vehicle = num
        self.ready_prompt = True


    def reset_play_state(self):
        self.vehicle_choice = ""
        self.selected_vehicle = None
        self.car = None
        self.ready_prompt = False
        self.countdown_active = False
        self.countdown_start_ms = 0
        self.race_active = False
        self.race_start_ms = 0
        self.race_end_ms = 0
        self.final_time_ms = None
        self.show_final_time = False
        self.lap_started = False
        self.game_over = False
        self.confirm_back = False


    def update(self):
        if not self.car:
            return

        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # Countdown handling
        if self.countdown_active and not self.race_active:
            elapsed = (now - self.countdown_start_ms) / 1000
            if elapsed >= 5:
                self.countdown_active = False
                self.race_active = True
                self.race_start_ms = now
                self.lap_started = True

        # Move car only during race
        if self.race_active and not self.game_over:
            self.car.update(keys)

        # Collision detection
        if self.race_active and not self.game_over:
            if self.collision_system.check_collision(self.car):
                self.game_over = True
                self.race_active = False
                self.countdown_active = False

        # Lap finish detection
        if self.race_active and self.lap_started:
            _, car_rect = self.car.get_mask_and_rect()
            near_center = abs(car_rect.centerx - self.game.current_size[0] // 2) < max(40, self.game.current_size[0] // 20)
            if near_center and car_rect.centery <= self.start_line_y:
                self.race_active = False
                self.race_end_ms = now
                self.final_time_ms = self.race_end_ms - self.race_start_ms
                self.show_final_time = True
                self.lap_started = False

    def draw(self, surface):
        surface.fill((0, 0, 0))
        size = self.game.current_size
        font = self.game.font
        large_font = self.game.large_font
        small_font = self.game.small_font

        # Draw track
        if self.track_surface:
            tx = (size[0] - self.track_surface.get_width()) // 2
            surface.blit(self.track_surface, (tx, 0))

        # Vehicle selection prompt
        if self.selected_vehicle is None:
            prompt = font.render("Enter vehicle (1-4) then press Enter:", True, (255, 255, 255))
            surface.blit(prompt, (20, 20))
            txt = font.render(self.vehicle_choice, True, (255, 200, 200))
            surface.blit(txt, (20, 60))

        # Draw car
        if self.car:
            self.car.draw(surface)

        now = pygame.time.get_ticks()

        # Countdown overlay
        if self.countdown_active and not self.race_active:
            elapsed = (now - self.countdown_start_ms) / 1000
            remaining = max(0, 5 - int(elapsed))
            cnt_text = large_font.render(str(remaining if remaining > 0 else 0), True, (255, 255, 0))
            surface.blit(cnt_text, ((size[0] - cnt_text.get_width()) // 2, (size[1] - cnt_text.get_height()) // 2))

        # READY prompt overlay
        if self.ready_prompt and not self.countdown_active and not self.race_active and not self.game_over:
            snap = surface.copy()
            surface.blit(blur_surface(snap, 6), (0, 0))
            overlay = pygame.Surface(size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            surface.blit(overlay, (0, 0))
            title = large_font.render("ARE YOU READY", True, (255, 255, 255))
            sub1 = font.render("Left click: YES", True, (200, 255, 200))
            sub2 = font.render("Right click: NO", True, (255, 200, 200))
            surface.blit(title, ((size[0] - title.get_width()) // 2, size[1] // 2 - 80))
            surface.blit(sub1, ((size[0] - sub1.get_width()) // 2, size[1] // 2 - 10))
            surface.blit(sub2, ((size[0] - sub2.get_width()) // 2, size[1] // 2 + 30))

        # Race timer
        if self.race_active:
            t_ms = now - self.race_start_ms
            s = t_ms // 1000
            ms = t_ms % 1000
            timer_surf = small_font.render(f"{s}.{ms:03d}s", True, (255, 255, 255))
            surface.blit(timer_surf, (10, size[1] - timer_surf.get_height() - 10))

        # GAME OVER
        if self.game_over:
            go = font.render("GAME OVER", True, (255, 20, 20))
            surface.blit(go, ((size[0] - go.get_width()) // 2, size[1] // 2))

        # Final time overlay
        if self.show_final_time and self.final_time_ms is not None:
            snap = surface.copy()
            surface.blit(blur_surface(snap, 4), (0, 0))
            overlay = pygame.Surface(size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            surface.blit(overlay, (0, 0))
            s = self.final_time_ms // 1000
            ms = self.final_time_ms % 1000
            final_str = f"{s}.{ms:03d}s"
            big_time = large_font.render(final_str, True, (255, 255, 0))
            good = large_font.render("GOOD RACE", True, (200, 255, 200))
            surface.blit(big_time, ((size[0] - big_time.get_width()) // 2, size[1] // 2 - 60))
            surface.blit(good, ((size[0] - good.get_width()) // 2, size[1] // 2 + 10))

        # Confirm back overlay
        if self.confirm_back:
            snap = surface.copy()
            surface.blit(blur_surface(snap, 8), (0, 0))
            overlay = pygame.Surface(size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            surface.blit(overlay, (0, 0))
            m1 = font.render("Return to main menu?", True, (255, 255, 255))
            m2 = font.render("Press ESC again to return, or click to continue.", True, (200, 200, 200))
            surface.blit(m1, ((size[0] - m1.get_width()) // 2, size[1] // 2 - 30))
            surface.blit(m2, ((size[0] - m2.get_width()) // 2, size[1] // 2 + 10))
