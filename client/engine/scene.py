import glm
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
            Mesh("client/assets/objs/planes/Plane 01/Plane 01.obj", self)
        ])

        self.terrain = Terrain(self)

        self.camera.target = self.plane.transform.position
    
    def update(self):
        self.camera.update()
        self.plane.update()
        self.terrain.update()

    def render(self):
        self.plane.render()
        self.terrain.render()