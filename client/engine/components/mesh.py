import copy
from .component import Component
import numpy as np
import pygame
import moderngl

class Mesh(Component):
    def __init__(self, path, scene, shaders_name="default", shaders_types="vf", shader_uniforms=["u_texture_0", "distance_of_view", "camPos", "fog"]):
        self.ctx:moderngl.Context = scene.ctx
        self.shader_uniforms = shader_uniforms
        self.scene = scene
        self.shaders_name = shaders_name
        self.shaders_types = shaders_types
        self.path = type(path)
        if isinstance(path, str):
            self.vertices, self.texture = self.load_obj(path)
        else:
            self.vertices, self.texture = path

        self.vbo = self.ctx.buffer(self.vertices)
        self.shader_program = self.get_shader_program()
        self.vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f 3f', 'in_texcoord_0', "in_normal", 'in_position')])
        if "u_texture_0" in self.shader_uniforms:
            self.shader_program['u_texture_0'] = 0
            self.texture.use()
        self.shader_program['m_proj'].write(scene.camera.m_proj)
    
    def get_texture(self, path):
        if path:
            texture = pygame.image.load(path).convert()
        else:
            texture = pygame.Surface((128, 128))
            texture.fill((255, 0, 0))
        texture = pygame.transform.flip(texture, False, True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pygame.image.tostring(texture, 'RGB'))

        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        texture.build_mipmaps()
        try:
            texture.anisotrophy = self.scene.app.settings.anisotrophy
        except:
            texture.anisotrophy = self.scene.settings.anisotrophy
        
        return texture

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def update(self, m_model):
        self.shader_program['m_view'].write(self.scene.camera.m_view)
        self.shader_program['m_model'].write(m_model)

    def get_shader_program(self):
        shaders = {}
        if 'v' in self.shaders_types:
            with open(f'client/shaders/{self.shaders_name}.vert', 'r') as f:
                shaders['vertex_shader'] = f.read()
        if 'f' in self.shaders_types:
            with open(f'client/shaders/{self.shaders_name}.frag', 'r') as f:
                shaders['fragment_shader'] = f.read()
        if 'g' in self.shaders_types:
            with open(f'client/shaders/{self.shaders_name}.geom', 'r') as f:
                shaders['geometry_shader'] = f.read()
        if 't' in self.shaders_types:
            with open(f'client/shaders/{self.shaders_name}.tesc', 'r') as f:
                shaders['tess_control_shader'] = f.read()
            with open(f'client/shaders/{self.shaders_name}.tese', 'r') as f:
                shaders['tess_evaluation_shader'] = f.read()

        prog = self.ctx.program(**shaders)

        return prog
    
    def render(self):
        self.texture.use()
        self.vao.render()
    

class TestMesh(Mesh):
    def __init__(self, hitbox, scene):
        self.ctx:moderngl.Context = scene.ctx
        self.scene = scene

        self.shaders_types = "vf"
        self.shaders_name = "explosion"
        self.shader_program = self.get_shader_program()

        bottom = hitbox[0]
        top = hitbox[1]
        right = hitbox[2]
        left = hitbox[3]
        front = hitbox[4]
        back = hitbox[5]

        self.vbo = self.ctx.buffer(np.array([
                                             back, top, left,
                                             back, bottom, right,
                                             back, top, right,
                                            
                                             back, top, left,
                                             back, bottom, left,
                                             back, bottom, right,

                                             front, top, left,
                                             front, top, right,
                                             front, bottom, right,
                                            
                                             front, top, left,
                                             front, bottom, right,
                                             front, bottom, left,

                                             front, top, left,
                                             front, bottom, left,
                                             back, top, left,

                                             back, bottom, left,
                                             back, top, left,
                                             front, bottom, left,

                                             front, top, right,
                                             back, top, right,
                                             front, bottom, right,

                                             back, bottom, right,
                                             front, bottom, right,
                                             back, top, right,

                                             front, top, left,
                                             back, top, left,
                                             back, top, right,

                                             front, top, right,
                                             front, top, left,
                                             back, top, right,

                                             front, bottom, left,
                                             back, bottom, right,
                                             back, bottom, left,

                                             front, bottom, right,
                                             back, bottom, right,
                                             front, bottom, left,
                                            ], dtype='f4'))
        
        self.vao = self.ctx.simple_vertex_array(self.shader_program, self.vbo, 'in_position')

        self.shader_program['m_proj'].write(scene.camera.m_proj)

    def update(self, m_model):
        self.shader_program['m_view'].write(self.scene.camera.m_view)
        self.shader_program['m_model'].write(m_model)

    def render(self):
        self.vao.render()