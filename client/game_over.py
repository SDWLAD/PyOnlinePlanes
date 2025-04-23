import pygame

from ui.text_box import TextBox
from ui.button import Button

class GameOver:
    def __init__(self, app, distance):
        self.screen_size = app.settings.window_size
        self.app = app


        self.back_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/back.png", lambda: self.app.change_scene("menu"), app.ctx)
        self.shop_button = Button(pygame.Rect(10, 70, 200, 100), "client/assets/buttons/shop.png", lambda: self.app.change_scene("shop"), self.app.ctx)

        self.distance_box =    TextBox(pygame.Rect(820,120, 520, 100), f"Відстань пройдено: {distance}", app.ctx)

    def update(self):...

    def render(self):
        self.back_button.render()
        self.shop_button.render()
        
        self.distance_box.render()

    def check_event(self, event):
        self.back_button.handle_event(event)
        self.shop_button.handle_event(event)