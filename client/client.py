from shop import ShopMenu
from menu import MainMenu
from settings import ClientSettings
from utils.singleton import Singleton
from engine.scene import Scene
import moderngl
import pygame

class Client(metaclass=Singleton):
    def __init__(self, client_settings=ClientSettings()):
        pygame.init()
        
        self.set_settings(client_settings)
        self.ctx = moderngl.create_context()
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND) 

        self.scenes = {
            "menu" : MainMenu(self),
            "shop" : [ShopMenu, self],
            "main" : [Scene, "main", self],
        }
        self.active_scene="menu"

    def change_scene(self, name, *args):
        self.active_scene = name
        scene = self.scenes[self.active_scene]
        if isinstance(scene, list):
            self.scenes[self.active_scene] = scene.pop(0)(*scene, *args)

    def set_settings(self, client_settings):
        self.settings = client_settings
        self.screen = pygame.display.set_mode(self.settings.window_size, *self.settings.window_args)
        pygame.display.set_caption(self.settings.window_title)
        if self.settings.window_icon: 
            pygame.display.set_icon(self.settings.window_icon)
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.scenes[self.active_scene].update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            self.scenes[self.active_scene].check_event(event)
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.ctx.clear(0., 0.56, 1.0)
        self.scenes[self.active_scene].render()
        pygame.display.flip()

if __name__ == "__main__":
    client = Client()
    client.run()