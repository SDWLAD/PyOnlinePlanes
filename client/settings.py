import pygame

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