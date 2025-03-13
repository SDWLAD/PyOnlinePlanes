import moderngl
import numpy as np
import pygame
from .components.mesh import Mesh
from .components.transform import Transform
from .game_object import GameObject
import glm


class Terrain(GameObject):
    def __init__(self, app, components=None, size=(1000,1000,2)):
        if components is None:
            components = [
                Transform(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0), glm.vec3(1))
            ]
        super().__init__(app, components)

        self.size = size

        ground_vertex_data =   [0, 0, 0, 1, 0, 0, 0, 0,
                                0,  100, 0, 1, 0, 0, 0, 1000,
                                100,  0, 0, 1, 0, 1000, 0, 0,
                                0., 100, 0, 1, 0, 0, 0, 1000,
                                100,100, 0, 1, 0, 1000, 0, 1000,
                                100, 0., 0, 1, 0, 1000, 0, 0,
                                ]
        
        ground_vertex_data = np.array(ground_vertex_data, dtype='f4')
        ground_image = pygame.Surface((64, 64))
        texture = self.app.ctx.texture(size=ground_image.get_size(), components=3, data=pygame.image.tostring(ground_image, 'RGB'))

        self.components.append(Mesh([ground_vertex_data, texture], self.app))