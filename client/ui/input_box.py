import moderngl
from .widget import Widget
import pygame
import copy
import glm


class InputBoxVariable:
    def __init__(self, var_name, variable):
        self.var_name = var_name
        self.variable = variable

class InputBox(Widget):
    def __init__(self, rect, variable, ctx):
        self.variable = variable

        self.old_texture = pygame.transform.scale(pygame.image.load("client/assets/buttons/input_box.png").convert_alpha(), (rect.size))
        self.original_texture = copy.copy(self.old_texture)

        self.label_font = pygame.font.Font("client/assets/fonts/Tiny5.ttf", 80)
        self.label = self.label_font.render(self.variable.variable , True, (255, 255, 255))
        self.label_rect = self.label.get_rect()
        self.label_rect.topleft = (5, 5)
        self.active = False

        self.original_texture.blit(self.label, self.label_rect)

        super().__init__(rect, [self.original_texture], ctx)

    def update(self):
        self.label_rect.w = max(200, self.label_rect.w+10)

    def update_texture(self):
        self.original_texture = copy.copy(self.old_texture)
        self.original_texture.blit(self.label, self.label_rect)

        texture = self.ctx.texture(size=self.original_texture.get_size(), components=4, data=pygame.image.tostring(self.original_texture, 'RGBA'))
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        self.textures[0] = texture

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.variable.variable = self.variable.variable[:-1]
                else:
                    self.variable.variable += event.unicode
                self.label = self.label_font.render(self.variable.variable , True, (255, 255, 255))
                self.update_texture()