import glm
import pygame
from ui.button import Button


class ShopMenu:
    def __init__(self, app):
        self.app = app
        self.screen_size = app.settings.window_size
        self.back_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/back.png", lambda: self.app.change_scene("menu"), self.app.ctx)

        self.planes_buttons = []
        self.planes_buttons.append(Button(
            pygame.Rect(10, self.screen_size[1]-110, 100, 100),
            "/mnt/files/projects/Python/Pygame/PyOnlinePlanes/client/assets/objs/planes/Plane 01/icon.png",
            lambda x=0: x,
            self.app.ctx
        ))
        self.planes_buttons[0].__setattr__("start_rect", self.planes_buttons[0].rect)

    def update(self): ...

    def render(self):
        self.back_button.render()
        for j in self.planes_buttons: 
            j.render()

    def check_event(self, event):
        self.back_button.handle_event(event)
        for j in self.planes_buttons: 
            j.handle_event(event)