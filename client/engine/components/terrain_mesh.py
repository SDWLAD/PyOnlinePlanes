import numpy as np
from .mesh import Mesh
import moderngl

class TerrainMesh(Mesh):
    def __init__(self, scene, vertices, indices, texture):
        self.ctx:moderngl.Context = scene.ctx
        self.scene = scene

        self.shaders_types = "vf"
        self.shaders_name = "terrain"
        self.shader_program = self.get_shader_program()

        self.texture = texture
        self.vbo = self.ctx.buffer(vertices)
        self.ibo = self.ctx.buffer(indices)
        self.vao = self.ctx.simple_vertex_array(self.shader_program, self.vbo, "data", index_buffer=self.ibo)
        self.shader_program['m_proj'].write(scene.camera.m_proj)
        self.shader_program['texture_0'] = 0

    def update(self, m_model):
        self.shader_program['m_view'].write(self.scene.camera.m_view)
        self.shader_program['m_model'].write(m_model)

    def render(self):
        self.texture.use(0)
        self.vao.render(moderngl.TRIANGLE_STRIP)