import numpy as np
import pygame

from .animator import Animation
from .components.transform import Transform
from .game_object import GameObject
from .components.mesh import Mesh
from engine.camera import Camera
import moderngl
import glm


class BackgroundScene:
    def __init__(self, name, app):
        self.name = name
        self.ctx = app.ctx
        self.app = app
        
        self.camera = Camera(app)
        self.camera.position = glm.vec3(8, 38, 8)
        
        self.plane = GameObject(self, [
            Transform(glm.vec3(0, 30, 0), glm.vec3(0, 0, 0), glm.vec3(1, 1, 1)),
            Mesh("client/assets/objs/planes/Plane 01/Plane 01.obj", self)
        ])

        self.camera_end_animation = Animation([(0, glm.vec3(*self.plane.transform.position)), (2, glm.vec3(0, 0, 0))])

        self.planes_meshes = [Mesh(f"client/assets/objs/planes/Plane 0{i}/Plane 0{i}.obj", self) for i in range(1, 7)]


        self.plane_speed = 0.5
        self.camera.target = self.plane.transform.position

        ground_vertex_data =   [0, 0, 0, 1, 0, 0, 0, 0,
                                0,  100, 0, 1, 0, 0, 0, 1000,
                                100,  0, 0, 1, 0, 1000, 0, 0,
                                0., 100, 0, 1, 0, 0, 0, 1000,
                                100,100, 0, 1, 0, 1000, 0, 1000,
                                100, 0., 0, 1, 0, 1000, 0, 0,
                                ]
        
        ground_vertex_data = np.array(ground_vertex_data, dtype='f4')
        ground_image = pygame.image.load("client/assets/grounds/ground0.webp").convert()
        texture = self.app.ctx.texture(size=ground_image.get_size(), components=3, data=pygame.image.tostring(ground_image, 'RGB'))
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        self.ground = GameObject(self, [
            Transform(glm.vec3(-500, 0, -500), glm.vec3(0, 0, 0), glm.vec3(10, 1, 10)),
            Mesh([ground_vertex_data, texture], self)
        ])

        self.offset = glm.vec3(2, 1, 0)
        self.radius = 8

    def play_end_animation(self):
        self.camera_end_animation = Animation([(0, 8), (4, 0), (4, lambda:self.app.change_scene("main"))], "ease_in_back")
        self.camera_end_animation.active = True


    def update(self):
        self.camera.update()

        angle = pygame.time.get_ticks() * 0.0001

        pos = self.plane.transform.position + self.offset

        if self.camera_end_animation.active: 
            self.camera_end_animation.update()
            self.radius = self.camera_end_animation.get_value()

        self.camera.position.x = self.plane.transform.position.x + self.radius * np.cos(angle)
        self.camera.position.z = self.plane.transform.position.z + self.radius * np.sin(angle)
        self.camera.position.y = pos.y + self.radius*0.8

        self.camera.target = pos

        self.plane.transform.position.x += self.plane_speed

        self.plane.update()
        self.ground.update()
    
    def render(self):
        self.plane.render()
        self.ground.render()

    def __repr__(self):
        return f'BackgroundScene(name={self.name})'