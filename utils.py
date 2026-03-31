import pygame

def scaled(surf, size):
    return pygame.transform.smoothscale(surf, size)

def pct_to_rect(pct, size):
    x = int(pct[0] * size[0])
    y = int(pct[1] * size[1])
    w = int(pct[2] * size[0])
    h = int(pct[3] * size[1])
    return pygame.Rect(x, y, w, h)

def blur_surface(surface, amount=8):
    if amount <= 1:
        return surface.copy()
    scale = 1.0 / amount
    sz = surface.get_size()
    small = pygame.transform.smoothscale(
        surface,
        (max(1, int(sz[0]*scale)), max(1, int(sz[1]*scale)))
    )
    return pygame.transform.smoothscale(small, sz)
