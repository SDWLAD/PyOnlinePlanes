import pygame
import moderngl
import numpy as np


class Widget:
    def __init__(self, rect, texture_path, ctx):
        self.rect = rect
        self.ctx:moderngl.Context = ctx

        self.texture = 0
        self.textures = []
        if isinstance(texture_path, list):
            for i in range(len(texture_path)):
                if isinstance(texture_path[i], str):
                    texture = pygame.image.load(texture_path[i]).convert_alpha()
                else:
                    texture = texture_path[i]
                texture = self.ctx.texture(size=texture.get_size(), components=4, data=pygame.image.tostring(texture, 'RGBA'))
                texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
                self.textures.append(texture)
        else:
            if isinstance(texture_path, str):
                texture = pygame.image.load(texture_path).convert_alpha()
            else:
                texture = texture_path
            texture = self.ctx.texture(size=texture.get_size(), components=4, data=pygame.image.tostring(texture, 'RGBA'))
            texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
            self.textures.append(texture)

        self.get_verticies()        
        self.inin_vao()
    
    def get_verticies(self):
        w_size = (1366, 768)

        left = self.rect.left / w_size[0] * 2 - 1
        right = self.rect.right / w_size[0] * 2 - 1
        top = self.rect.top / w_size[1] * 2 - 1
        bottom = self.rect.bottom / w_size[1] * 2 - 1

        self.vertex_data = np.array([
            left, -top, 0.0, 0.0,
            left, -bottom, 0.0, 1.0,
            right, -top, 1.0, 0.0,
            right, -bottom,  1.0, 1.0
        ], dtype='f4')

    def inin_vao(self):
        with open('client/shaders/ui.vert', 'r') as f: self.vertex_shader  = f.read()
        with open('client/shaders/ui.frag', 'r') as f: self.fragment_shader= f.read()
        program = self.ctx.program(vertex_shader=self.vertex_shader, fragment_shader=self.fragment_shader)
        self.vao = self.ctx.vertex_array(program, [(self.ctx.buffer(self.vertex_data), '2f 2f', 'in_vert', 'in_texcoord')], index_buffer=None)

    def update(self):...

    def render(self):
        self.textures[self.texture].use(location=0)
        self.vao.render(moderngl.TRIANGLE_STRIP)