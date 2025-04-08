import numpy as np
import pygame
from .mesh import Mesh
import moderngl

class ExplosionMesh(Mesh):
    def __init__(self, scene):
        self.ctx:moderngl.Context = scene.ctx
        self.scene = scene

        self.shaders_types = "vf"
        self.shaders_name = "explosion"
        self.shader_program = self.get_shader_program()

        texture = pygame.image.load("client/assets/explosion/explosion.tif").convert_alpha()
        self.texture = self.ctx.texture(texture.get_size(), components=4, data=pygame.image.tostring(texture, 'RGBA'))

        self.vbo = self.ctx.buffer(np.array([0,-5,-5, 0, 1,
                                             0,-5, 5, 1, 1,
                                             0, 5, 5, 1, 0,
                                             0, 5,-5, 0, 0,
                                             0,-5,-5, 0, 1,
                                             0, 5, 5, 1, 0,
                                            ], dtype='f4'))
        
        self.vao = self.ctx.simple_vertex_array(self.shader_program, self.vbo, 'in_position', "in_uv")

        self.shader_program['u_texture_0'].value = 0
        self.shader_program['m_proj'].write(scene.camera.m_proj)
        self.shader_program['u_size'].value = 6

        self.tick = 0

    def update(self, m_model):
        self.tick += 0.1
        if self.tick >= 30: self.tick = 30
        self.shader_program['m_view'].write(self.scene.camera.m_view)
        self.shader_program['m_model'].write(m_model)
        self.shader_program['u_offset'].value = (int(self.tick)/6, int(int(self.tick)/6)/6)