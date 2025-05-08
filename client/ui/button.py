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

class LegacyButton:
    def __init__(self, rect, texture:str, func):
        self.rect = rect
        self.texture = pygame.transform.scale(pygame.image.load(texture).convert_alpha(), self.rect.size)
        try:
            self.texture_n = pygame.transform.scale(pygame.image.load(str(texture.split(".")[0])+"_n.png").convert_alpha(), self.rect.size)
        except:
            self.texture_n = self.texture
            
        self.current_texture = self.texture
        self.func = func

    def draw(self, screen):
        screen.blit(self.current_texture, self.rect)

    def update(self):...

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_texture = self.texture_n
            else:
                self.current_texture = self.texture
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.func()

class PlaneButton(LegacyButton):
    def __init__(self, rect, texture, func, plane_id):
        self.pos = rect.center
        self.plane_id = plane_id
        self.rect = rect
        self.texture = pygame.transform.scale(pygame.image.load(texture).convert_alpha(), self.rect.size)
        self.texture_n = self.texture
        self.current_texture = self.texture
        self.func = func

    def update(self, offset):
        self.rect.center = self.pos + offset
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_texture = self.texture_n
            else:
                self.current_texture = self.texture
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.func()