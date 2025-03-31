import glm
import pygame
import copy

from .widget import Widget

class CheckBoxVariable:
    def __init__(self, var_name, variable):
        self.var_name = var_name
        self.variable = variable

class CheckBox(Widget):
    def __init__(self, rect, variable, ctx):
        self.variable = variable

        icon = pygame.image.load("client/assets/buttons/button.png").convert_alpha()
        icon_OK = pygame.image.load("client/assets/buttons/button_OK.png").convert_alpha()

        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        surf.blit(pygame.transform.scale(icon, (rect.height, rect.height)), (0, 0))

        self.label_font = pygame.font.Font("client/assets/fonts/Tiny5.ttf", 48)
        self.label = self.label_font.render(self.variable.var_name , True, (255, 255, 255))
        self.label_rect = self.label.get_rect()
        self.label_rect.centery = rect.height//2
        self.label_rect.right = rect.width
        surf.blit(self.label, self.label_rect)


        surf2 = copy.copy(surf)
        surf2.blit(pygame.transform.scale(icon_OK, (rect.height, rect.height)), (0, 0))

        super().__init__(rect, [surf2, surf], ctx)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.variable.variable = not self.variable.variable
                self.texture = int(not self.texture)