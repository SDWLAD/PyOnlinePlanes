import pygame
from ui.button import Button


class MainMenu:
    def __init__(self, app):
        self.app = app
        screen_size = app.settings.window_size
        buttons_x = screen_size[0]-250

        self.play_button = Button(pygame.Rect(buttons_x, 100, 200, 100), "client/assets/buttons/play.png", lambda: self.app.change_scene("main"), self.app.ctx)
    
    def update(self):...

    def render(self):
        self.play_button.render()

    def check_event(self, event):
        self.play_button.handle_event(event)