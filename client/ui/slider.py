import glm
import moderngl
import pygame
import copy

from .widget import Widget

class SliderVariable:
    def __init__(self, var_name, variable, min_value, max_value):
        self.var_name = var_name
        self.variable = variable
        self.min_value = min_value
        self.max_value = max_value

class Slider(Widget):
    def __init__(self, rect, variable, ctx):
        self.variable = variable

        self.local_value = (self.variable.variable - self.variable.min_value) / (self.variable.max_value - self.variable.min_value)
        self.pressed = False
        self.line_rect = copy.copy(rect)
        self.line_rect.height /= 5
        self.b_rect = pygame.Rect(glm.mix(0, rect.width-rect.height, self.local_value), 0, rect.height, rect.height)
        self.line_texture = pygame.transform.scale(pygame.image.load("client/assets/buttons/slider.png").convert_alpha(), (self.line_rect.size))
        self.button_texture = pygame.transform.scale(pygame.image.load("client/assets/buttons/button.png").convert_alpha(), (self.b_rect.size))

        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        surf.blit(self.line_texture, (0, rect.height//2-self.line_rect.height//2))
        surf.blit(self.button_texture, self.b_rect)

        self.label_font = pygame.font.Font("client/assets/fonts/Tiny5.ttf", 24)
        self.label = self.label_font.render(f"{self.variable.var_name}: {self.variable.variable}", True, (255, 255, 255))
        self.label_rect = self.label.get_rect()

        self.label_rect.centerx = rect.width//2
        self.label_rect.centery = rect.height//2

        surf.blit(self.label, self.label_rect)

        super().__init__(rect, [surf], ctx)

    def set_variable(self):
        self.variable.variable = int(glm.mix(self.variable.min_value, self.variable.max_value, self.local_value))

    def update_texture(self):
        surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        surf.blit(self.line_texture, (0, self.rect.height//2-self.line_rect.height//2))
        surf.blit(self.button_texture, self.b_rect)
        self.label = self.label_font.render(f"{self.variable.var_name}: {self.variable.variable}", True, (255, 255, 255))
        surf.blit(self.label, self.label_rect)

        texture = self.ctx.texture(size=surf.get_size(), components=4, data=pygame.image.tostring(surf, 'RGBA'))
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        self.textures[0] = texture


    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.pressed:
            self.local_value = glm.clamp((mouse_pos[0]-self.rect.left)/self.rect.width, 0, 1)
            self.b_rect.x = glm.mix(0, self.rect.width-self.rect.height, self.local_value)
            self.update_texture()
            self.set_variable()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos): self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP: self.pressed = False