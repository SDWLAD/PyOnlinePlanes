from settings import ClientSettings
from utils.singleton import Singleton
import numpy as np
import moderngl
import pygame

class Client(metaclass=Singleton):
    def __init__(self, client_settings=ClientSettings()):
        pygame.init()
        
        self.set_settings(client_settings)
        self.ctx = moderngl.create_context()
    
    def set_settings(self, client_settings):
        self.settings = client_settings
        self.screen = pygame.display.set_mode(self.settings.window_size, *self.settings.window_args)
        pygame.display.set_caption(self.settings.window_title)
        if self.settings.window_icon: 
            pygame.display.set_icon(self.settings.window_icon)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.ctx.clear(0.1, 0.1, 0.1)

if __name__ == "__main__":
    client = Client()
    client.run()