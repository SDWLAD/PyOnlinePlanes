from settings import ClientSettings, SettingsMenu
from engine.bg_scene import BackgroundScene
from utils.singleton import Singleton
from sound import SoundController
from engine.scene import Scene
from game_over import GameOver
from menu import MainMenu
from shop import ShopMenu
import moderngl as mgl
import socket
import pygame
import json


class Client(metaclass=Singleton):
    def __init__(self, client_settings=ClientSettings()):
        pygame.init()
        
        self.set_settings(client_settings)
        self.init()

    def set_settings(self, client_settings):
        self.settings = client_settings
        self.screen = pygame.display.set_mode(self.settings.window_size, *self.settings.window_args)
        pygame.display.set_caption(self.settings.window_title)
        if self.settings.window_icon: 
            pygame.display.set_icon(self.settings.window_icon)
        self.clock = pygame.time.Clock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def init(self):
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND) 
        self.ctx.gc_mode = 'auto'
        self.ctx.wireframe = False
        
        with open("client/planes.json", "r") as f:
            self.planes = json.load(f)
        self.selected_plane = self.planes[list(self.planes.keys())[0]]

        self.background = BackgroundScene("background", self)

        self.scenes = {
            "menu" : MainMenu(self),
            "shop" : [ShopMenu, self],
            "main" : [Scene, "main", self],
            "game_over" : [GameOver, self],
            "settings" : [SettingsMenu, self, self.settings],
        }
        self.active_scene="menu"

        self.sound_controller = SoundController()
        self.sound_controller.load_music("main", "client/assets/sounds/MainOST.mp3")

    def set_plane(self, plane):
        self.selected_plane = plane
        self.background.plane.components[1] = self.background.planes_meshes[plane["id"]-1]

    def change_scene(self, name, *args):
        if name=="main": 
            self.active_scene = name
            self.scenes[self.active_scene] = Scene("main", self)
        elif self.active_scene == "main":
            self.scenes[self.active_scene].disconnect() 

        self.active_scene = name
        scene = self.scenes[self.active_scene]
        if isinstance(scene, list):
            self.scenes[self.active_scene] = scene.pop(0)(*scene, *args)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

            pygame.display.set_caption(f"{self.settings.window_title}: {int(self.clock.get_fps())}") 
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            self.scenes[self.active_scene].check_event(event)
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        if self.active_scene != "main": self.background.update()
        self.scenes[self.active_scene].update()

    def render(self):
        self.ctx.clear(0., 0.56, 1.0)
        if self.active_scene != "main": self.background.render()
        self.scenes[self.active_scene].render()
        pygame.display.flip()

if __name__ == "__main__":
    client = Client()
    client.run()