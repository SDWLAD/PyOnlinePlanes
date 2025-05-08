import pygame

from .widget import Widget

class Panel(Widget):
    def __init__(self, rect, color, ctx, **roundings):
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surf, color, surf.get_rect(), 0, **roundings)
        super().__init__(rect, surf, ctx)