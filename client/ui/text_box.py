import pygame
import copy

from .widget import Widget

class TextBox(Widget):
    def __init__(self, rect, text, ctx):

        surf = pygame.Surface(rect.size, pygame.SRCALPHA)

        self.label_font = pygame.font.Font("client/assets/fonts/Tiny5.ttf", 48)
        self.label = self.label_font.render(text , True, (255, 255, 255))
        self.label_rect = self.label.get_rect()
        self.label_rect.centery = rect.height//2
        self.label_rect.right = rect.width
        surf.blit(self.label, self.label_rect)

        super().__init__(rect, surf, ctx)