import math
import pygame

class Car:
    def __init__(self, surf: pygame.Surface):
        self._orig = surf.convert_alpha()
        self._surf = self._orig.copy()

        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0          
        self.velocity = 0.0       


        self.max_speed = 10
        self.accel = 0.40
        self.brake = 0.70
        self.decel = 0.20
        self.steer_rate_fast = 1.9
        self.steer_rate_slow = 3.2

    def update(self, keys):

        steer = 0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: steer -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: steer += 1

        if abs(self.velocity) > 0.5:
            steer_amount = self.steer_rate_slow if abs(self.velocity) < 4 else self.steer_rate_fast
            self.angle += steer * steer_amount * (abs(self.velocity) / self.max_speed + 0.15)
            self.angle %= 360


        accel_input = 0
        if keys[pygame.K_UP]   or keys[pygame.K_w]: accel_input += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: accel_input -= 1

        if accel_input > 0:
            self.velocity += self.accel
        elif accel_input < 0:
            if self.velocity > 0:
                self.velocity -= self.brake
            else:
                self.velocity -= self.accel * 0.6 
        else:

            if abs(self.velocity) > self.decel:
                self.velocity -= math.copysign(self.decel, self.velocity)
            else:
                self.velocity = 0

        self.velocity = max(-self.max_speed * 0.45, min(self.max_speed, self.velocity))

        rad = math.radians(self.angle)
        self.x += self.velocity * math.cos(rad)
        self.y += self.velocity * math.sin(rad)

    def draw(self, surface: pygame.Surface):

        self._surf = pygame.transform.rotozoom(self._orig, -self.angle, 1.0)
        rect = self._surf.get_rect(center=(round(self.x), round(self.y)))
        surface.blit(self._surf, rect.topleft)
        return rect

    def get_mask_and_rect(self):
        rect = self._surf.get_rect(center=(round(self.x), round(self.y)))
        mask = pygame.mask.from_surface(self._surf)
        return mask, rect
