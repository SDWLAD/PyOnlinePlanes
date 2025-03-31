import pygame

from ui.check_box import CheckBox, CheckBoxVariable

from ui.button import Button

class ClientSettings:
    window_size = (1366, 768)
    window_args = [pygame.DOUBLEBUF | pygame.OPENGLBLIT]
    window_title = "Client"
    window_vsync = True
    window_icon = None
    window_fps = 60
    mouse_visible = False
    mouse_locked = True
    distance_of_view = 500

    def __init__(self):
        self.changeable = [
            CheckBoxVariable("window_vsync", self.window_vsync)
        ]

class SettingsMenu:
    def __init__(self, app, settings: ClientSettings):
        self.app = app
        self.screen_size = self.app.settings.window_size
        self.settings = settings

        self.generate_menu()

        self.back_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/back.png", lambda: app.change_scene("menu"), app.ctx)

    def generate_menu(self):
        self.sliders = []

        slider_size = (600, 100)

        for j,i in enumerate(self.settings.changeable):
            x_pos = 100
            y_pos = j*110

            if isinstance(i, CheckBoxVariable):
                self.sliders.append(CheckBox(pygame.Rect(x_pos, y_pos, *slider_size), i, self.app.ctx))

    def update(self):
        for i in self.sliders:
            i.update()
        for i in self.settings.changeable:
            if i.var_name in ClientSettings.__dict__:
                self.settings.__dict__[i.var_name] = i.variable

    def render(self):
        self.back_button.render()

        for i in self.sliders:
            i.render()

    def check_event(self, event):
        self.back_button.handle_event(event)
        for i in self.sliders:
            i.handle_event(event)