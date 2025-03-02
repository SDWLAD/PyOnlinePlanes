import numpy as np

from engine.camera import Camera

vertex_shader = """
#version 330 core
layout(location = 0) in vec2 in_position;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

# Fragment Shader
fragment_shader = """
#version 330 core
out vec4 fragColor;
void main() {
    fragColor = vec4(0.3, 0.6, 0.3, 1.0);
}
"""

class Scene:
    def __init__(self, name, app):
        self.name = name
        self.ctx = app.ctx
        self.app = app
        self.camera = Camera(app)
        
        prog = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )

        vertices = np.array([[-1, -1], [1, -1], [0, 1]], dtype='f4')
        vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.simple_vertex_array(prog, vbo, 'in_position')
    
    def update(self):
        self.camera.update()

    def render(self):
        self.vao.render()