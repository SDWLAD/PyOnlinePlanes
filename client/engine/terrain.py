import moderngl
import numpy as np
import pygame
from utils.world_generator import generate_landscape
from .components.terrain_mesh import TerrainMesh
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

        self.generate()

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def generate(self):
        self.terrain = generate_landscape(self.size, 128, 100, 6, 0.5, 2.0, 32)
        scale = int(self.size[0])
        size = int(self.size[0]/self.size[2])
    
        x = np.linspace(0, scale, size+1)[0:-1]
        y = np.linspace(0, scale, size+1)[0:-1]
        xx, zz = np.meshgrid(x, y)
        self.yy = np.zeros((size, size))

        self.yy = self.terrain[::self.size[2], ::self.size[2]]

        self.yy = np.where(self.yy <= 7, 7, self.yy)

        self.texture = np.zeros((size, size, 3), dtype=np.uint8)
        self.texture[self.yy > 45] = (255, 255, 255)
        self.texture[(self.yy > 40) & (self.yy <= 45)] = (97, 97, 97)
        self.texture[(self.yy > 10) & (self.yy <= 40)] = (0, 135, 0)
        self.texture[(self.yy > 7) & (self.yy <= 10)] = (199, 194, 56)
        self.texture[(self.yy == 7)] = (27, 59, 242)

        vertices = np.column_stack((zz.ravel(), self.yy.ravel(), xx.ravel()))

        normals = np.zeros_like(vertices)

        left = np.zeros((size*size, 3))
        right = np.zeros((size*size, 3))
        up = np.zeros((size*size, 3))
        down = np.zeros((size*size, 3))

        for idx in range(size, size*size - size):
            left[idx], right[idx] = vertices[idx - 1], vertices[idx + 1]
            up[idx], down[idx] = vertices[idx - size], vertices[idx + size]

        normal = np.cross(right - left, down - up)
        normals = normal / np.linalg.norm(normal, axis=1)[:,None]

        yaw = np.arctan2(normals[:,0], normals[:,2])
        pitch = np.arcsin(normals[:,1])

        normals = np.column_stack((yaw, pitch))

        vertices = np.hstack((self.yy.ravel()[:,None], normals)).astype('f4')

        indices = []
        for i in range(size - 1):
            if i % 2 == 0:
                for j in range(size):
                    indices.append((i + 1) * size + j)
                    indices.append(i * size + j)
            else:
                for j in reversed(range(size)):
                    indices.append(i * size + j)
                    indices.append((i + 1) * size + j)
        indices = np.array(indices, dtype='i4')

        texture_surface = pygame.surfarray.make_surface(self.texture)
        texture = self.app.ctx.texture(size=texture_surface.get_size(), components=3, data=pygame.image.tostring(texture_surface, 'RGB'))
        texture.filter = (moderngl.LINEAR, moderngl.LINEAR)


        self.components.append(TerrainMesh(self.app, vertices, indices, texture))