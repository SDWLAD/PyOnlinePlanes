from random import randint
import socket
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
import pickle


class Scene:
    def __init__(self, name, app):
        self.name = name
        self.ctx = app.ctx
        self.app = app
        self.connect()
        self.camera = Camera(app)
        self.player = Player(self, [
            Transform(glm.vec3(randint(0, 500), 100, randint(0, 500)), glm.vec3(0, 0, 0), glm.vec3(1, 1, 1))
        ])

        self.explosion = GameObject(self, [
            self.player.transform,
            ExplosionMesh(self)
        ])

        self.terrain = Terrain(self)

        self.pause_button = Button(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/settings.png", lambda: self.app.change_scene("menu"), self.app.ctx)
        self.players = {}
    

    def connect(self):
        host_str = self.app.settings.host.split(":")
        self.app.socket.connect((host_str[0], int(host_str[1])))

    def disconnect(self):
        self.app.socket.close()
        self.app.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def update_socket(self):
        try:
            players = pickle.loads(self.app.socket.recv(1024))
            if len(players) == 0 and len(self.players) != 0:
                self.player.game_over_animation.active=True
                self.disconnect()
                return

            for addr, pos in players.items():
                if addr not in self.players.keys():
                    self.players[addr] = GameObject(self, [Transform(glm.vec3(pos[0]), glm.vec3(pos[1]), glm.vec3(1)), Mesh(f"client/assets/objs/planes/Plane 0{pos[2]}/Plane 0{pos[2]}.obj", self)])
                    self.players[addr].__setattr__("hitbox", self.app.planes[f"Plane 0{pos[2]}"]["hitbox"])
                self.players[addr].transform.position = glm.vec3(pos[0])
                self.players[addr].transform.rotation = glm.vec3(pos[1])

            if len(self.players) > len(players):
                for i in self.players:
                    if i not in players.keys():
                        del self.players[i]

            data = [self.player.transform.position, self.player.transform.rotation, self.app.selected_plane["id"]]

            for i, j in self.players.items():
                if "game_over" in j.__dict__:
                    data.append(i)

            self.app.socket.send(pickle.dumps(data))
        except OSError:
            print("[ERROR] Socket closed.")

    def check_event(self, event):
        self.pause_button.handle_event(event)

    def update(self):
        self.camera.update()

        self.player.update(self.terrain)
        self.terrain.update()
        self.pause_button.update()
        if self.player.game_over_animation.active: self.explosion.update()

        for i in self.players.values(): i.update()

        self.update_socket()

    def render(self):
        self.player.render()

        for i in self.players.values(): i.render()

        self.terrain.render()
        if self.player.game_over_animation.active: self.explosion.render()
        self.pause_button.render()