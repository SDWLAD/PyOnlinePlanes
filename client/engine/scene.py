import numpy as np

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
        self.ctx = app.ctx
        self.app = app

        prog = self.ctx.program(
            vertex_shader=vertex_shader,
            # tess_control_shader=control_shader,
            # tess_evaluation_shader=evaluation_shader,
            fragment_shader=fragment_shader,
        )

        vertices = np.array([[-1, -1], [1, -1], [0, 1]], dtype='f4')
        vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.simple_vertex_array(prog, vbo, 'in_position')
    
    def render(self):
        self.vao.render()