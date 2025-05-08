import glm
import pygame
from ui.panel import Panel
from ui.button import Button


class NewShopMenu:
    def __init__(self, app):
        self.app = app
        self.screen_size = app.settings.window_size

        self.planes_panel = Panel(pygame.Rect(0, self.screen_size[1]-120, self.screen_size[0], 120), (255, 255, 255, 100), self.app.ctx)
        self.back_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/back.png", lambda: self.app.change_scene("menu"), self.app.ctx)
    
        self.buttons_offset = 0

        self.planes_buttons = []
        for i,j in enumerate(self.app.planes):
            self.planes_buttons.append(Button(
                pygame.Rect(10+(i)*110, self.screen_size[1]-110, 100, 100),
                self.app.planes[j]["path"]+"/icon.png",
                lambda j=j: app.set_plane(self.app.planes[j]),
                self.app.ctx
            ))
            self.planes_buttons[i].__setattr__("start_rect", self.planes_buttons[i].rect)

    def update(self):
        id = self.app.selected_plane["id"]
        pos = (id-1)*110
        self.buttons_offset = (glm.mix(self.buttons_offset, self.screen_size[0]//2-pos-60, 0.15))

    def render(self):
        self.back_button.render()
        for j in self.planes_buttons: 
            j.render()
        self.planes_panel.render()

    def check_event(self, event):
        self.back_button.handle_event(event)
        for j in self.planes_buttons: 
            j.handle_event(event)