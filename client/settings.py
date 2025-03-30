import pygame

from ui.button import Button

class ClientSettings:
    def __init__(self):
        self.window_size = (1366, 768)
        self.window_args = [pygame.DOUBLEBUF | pygame.OPENGLBLIT]
        self.window_title = "Client"
        self.window_vsync = True
        self.window_icon = None
        self.window_fps = 60
        self.mouse_visible = False
        self.mouse_locked = True
        self.distance_of_view = 500



class SettingsMenu:
    def __init__(self, app, settings: ClientSettings):
        self.app = app
        self.screen_size = self.app.settings.window_size
        self.settings = settings

        self.back_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/back.png", lambda: self.app.change_scene("menu"), self.app.ctx)

    def update(self): ...

    def render(self):
        self.back_button.render()

    def check_event(self, event):
        self.back_button.handle_event(event)