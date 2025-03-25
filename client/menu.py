import pygame
import sys
from ui.button import Button


class MainMenu:
    def __init__(self, app):
        self.app = app
        screen_size = app.settings.window_size
        buttons_x = screen_size[0]-250

        self.play_button = Button(pygame.Rect(buttons_x, 100, 200, 100), "client/assets/buttons/play.png", lambda: self.app.change_scene("main"), self.app.ctx)
        self.shop_button = Button(pygame.Rect(buttons_x, 250, 200, 100), "client/assets/buttons/shop.png", lambda: self.app.change_scene("shop"), self.app.ctx)
        self.exit_button = Button(pygame.Rect(buttons_x, 400, 200, 100), "client/assets/buttons/exit.png", lambda: sys.exit(0), self.app.ctx)
    
    def update(self):...

    def render(self):
        self.play_button.render()
        self.shop_button.render()
        self.exit_button.render()

    def check_event(self, event):
        self.play_button.handle_event(event)
        self.shop_button.handle_event(event)
        self.exit_button.handle_event(event)