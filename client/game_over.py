import pygame

from ui.text_box import TextBox
from ui.button import Button

class GameOver:
    def __init__(self, app, points, distance, all_bullets, score):
        self.screen_size = app.settings.window_size
        self.app = app


        self.back_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/back.png", lambda: self.app.change_scene("menu"), app.ctx)
        self.shop_button = Button(pygame.Rect(10, 70, 200, 100), "client/assets/buttons/shop.png", lambda: self.app.change_scene("shop"), self.app.ctx)

        self.points_box =      TextBox(pygame.Rect(820, 10, 520, 100), f"Літаків збито: {points}", app.ctx)
        self.distance_box =    TextBox(pygame.Rect(820,120, 520, 100), f"Відстань пройдено: {distance}", app.ctx)
        self.all_bullets_box = TextBox(pygame.Rect(820,230, 520, 100), f"Куль випущено: {all_bullets}", app.ctx)
        self.score_box =       TextBox(pygame.Rect(820,340, 520, 100), f"Рахунок: {score}", app.ctx)

    def update(self):...

    def render(self):
        self.back_button.render()
        self.shop_button.render()
        
        self.points_box.render()
        self.distance_box.render()
        self.all_bullets_box.render()
        self.score_box.render()

    def check_event(self, event):
        self.back_button.handle_event(event)
        self.shop_button.handle_event(event)