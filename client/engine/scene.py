import glm
import pygame

from ui.button import Button
from .terrain import Terrain
from .player import Player
from .components.transform import Transform
from .components.mesh import Mesh
from engine.camera import Camera

class Scene:
    def __init__(self, name, app):
        self.name = name
        self.ctx = app.ctx
        self.app = app
        self.camera = Camera(app)

        self.plane = Player(self, [
            Transform(glm.vec3(10), glm.vec3(0), glm.vec3(1)),
            Mesh(f"client/assets/objs/planes/Plane 0{app.selected_plane["id"]}/Plane 0{app.selected_plane["id"]}.obj", self)
        ])

        self.terrain = Terrain(self)

        self.pause_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/settings.png", lambda: self.app.change_scene("menu"), self.app.ctx)
        self.camera.target = self.plane.transform.position
    
    def check_event(self, event):
        self.pause_button.handle_event(event)

    def update(self):
        self.camera.update()

        self.plane.update()
        self.terrain.update()
        self.pause_button.update()

    def render(self):
        self.plane.render()
        self.terrain.render()
        self.pause_button.render()