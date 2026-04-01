import pygame

class CollisionSystem:
    def __init__(self, border_mask: pygame.Mask, border_offset: tuple[int, int]):
        self.border_mask = border_mask
        self.border_offset = border_offset
        self.mask_scale = 0.6
        self.crash_threshold = 50

    def check_collision(self, car) -> bool:
        if not self.border_mask or not car:
            return False

        car_mask, car_rect = car.get_mask_and_rect()

        scaled_surf = pygame.transform.smoothscale(
            car._surf if hasattr(car, "_surf") else car.surf,
            (int(car_rect.width * self.mask_scale), int(car_rect.height * self.mask_scale))
        )
        car_mask = pygame.mask.from_surface(scaled_surf)

        offset = (car_rect.left - self.border_offset[0], car_rect.top - self.border_offset[1])

        try:
            overlap_area = self.border_mask.overlap_area(car_mask, offset)
        except Exception:
            overlap_area = 0

        return overlap_area > self.crash_threshold
