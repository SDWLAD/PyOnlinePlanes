import pygame

from .widget import Widget

class Panel(Widget):
    def __init__(self, rect, color, ctx, **roundings):
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surf, color, surf.get_rect(), 0, **roundings)
        super().__init__(rect, surf, ctx)

class LegacyPanel:
    def __init__(self, rect, color, **roundings):
        self.rect = rect
        self.color = color
        self.texture = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(self.texture, color, self.texture.get_rect(), 0, **roundings)

    def draw(self, screen):
        screen.blit(self.texture, self.rect)

    def handle_event(self, event):
        pass