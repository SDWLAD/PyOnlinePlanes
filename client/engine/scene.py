from random import randint
import glm
import pygame

from ui.button import Button
from .components.explosion_mesh import ExplosionMesh
from .game_object import GameObject
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

        self.player = Player(self, [
            Transform(glm.vec3(randint(0, 500), 100, randint(0, 500)), glm.vec3(0, 0, 0), glm.vec3(1, 1, 1)),
            Mesh(f"client/assets/objs/planes/Plane 0{app.selected_plane["id"]}/Plane 0{app.selected_plane["id"]}.obj", self)
        ])

        self.explosion = GameObject(self, [
            self.player.transform,
            ExplosionMesh(self)
        ])

        self.terrain = Terrain(self)

        self.pause_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/settings.png", lambda: self.app.change_scene("menu"), self.app.ctx)
        self.camera.target = self.player.transform.position
    
    def check_event(self, event):
        self.pause_button.handle_event(event)

    def update(self):
        self.camera.update()

        self.player.update(self.terrain)
        self.terrain.update()
        self.pause_button.update()
        if self.player.game_over_animation.active: self.explosion.update()

    def render(self):
        self.player.render()
        self.terrain.render()
        self.pause_button.render()
        if self.player.game_over_animation.active: self.explosion.render()