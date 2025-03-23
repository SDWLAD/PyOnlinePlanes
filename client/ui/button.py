import pygame
from .widget import Widget


class Button(Widget):
    def __init__(self, rect, texture_path, callback, ctx):
        self.callback = callback
        super().__init__(rect, texture_path, ctx)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()