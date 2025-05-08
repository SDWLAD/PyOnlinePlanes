import glm
import pygame
from ui.panel import LegacyPanel
from ui.button import LegacyButton, PlaneButton
import glm
import pygame
import moderngl
import numpy as np


class ShopMenu:
    vertex_shader = """
    #version 330
    in vec2 in_vert;
    in vec2 in_texcoord;
    out vec2 v_texcoord;

    void main() {
        gl_Position = vec4(in_vert, 0.0, 1.0);
        v_texcoord = in_texcoord;
    }
    """

    fragment_shader = """
    #version 330
    uniform sampler2D Texture;
    in vec2 v_texcoord;
    out vec4 fragColor;

    void main() {
        fragColor = texture(Texture, v_texcoord);
    }
    """
    def __init__(self, app):
        self.app = app

        self.sub_surf = pygame.Surface((self.app.settings.window_size), pygame.SRCALPHA)
        self.surface = pygame.Surface((self.app.settings.window_size), pygame.SRCALPHA)
        self.surf_pos = glm.vec2(0, 0)

        self.texture = self.app.ctx.texture(app.settings.window_size, 4)  # Use 4 channels for RGBA
        self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.vertices = np.array([
            -1.0, -1.0, 0.0, 0.0,
            1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
            1.0,  1.0, 1.0, 1.0,
        ], dtype='f4')
        program = self.app.ctx.program(vertex_shader=self.vertex_shader, fragment_shader=self.fragment_shader)
        indices = np.array([0, 1, 2, 2, 1, 3], dtype='i4')
        vbo = self.app.ctx.buffer(self.vertices.tobytes())
        ibo = self.app.ctx.buffer(indices.tobytes())
        self.vao = self.app.ctx.vertex_array(
            program,
            [
                (vbo, '2f 2f', 'in_vert', 'in_texcoord')
            ],
            ibo
        )
        self.screen_size = app.settings.window_size

        self.planes_panel = LegacyPanel(pygame.Rect(0, self.screen_size[1]-120, self.screen_size[0], 120), (255, 255, 255, 100))
        self.plane_selector = LegacyPanel(pygame.Rect(self.screen_size[0]//2-25, self.screen_size[1]-20, 50, 10), (255, 255, 255, 100), border_radius=10)
        self.back_button = LegacyButton(pygame.Rect(10, 10, 50, 50), "client/assets/buttons/back.png", lambda: self.app.change_scene("menu"))

        self.buttons_offset = 0

        self.planes_buttons = []
        for i,j in enumerate(self.app.planes):
            self.planes_buttons.append(PlaneButton(
                pygame.Rect(10+(i)*110, self.screen_size[1]-110, 100, 100),
                self.app.planes[j]["path"]+"/icon.png",
                lambda j=j: app.set_plane(self.app.planes[j]),
                i+1
            ))

        self.characteristics_panel = LegacyPanel(pygame.Rect(self.screen_size[0] - 200, 0, 200, 100), (255, 255, 255, 100), border_bottom_left_radius=10)

    def update(self):
        id = self.app.selected_plane["id"]
        pos = (id-1)*110
        self.buttons_offset = (glm.mix(self.buttons_offset, self.screen_size[0]//2-pos-60, 0.15))
        
        y_pos = glm.abs(1-glm.abs(self.planes_buttons[id-1].rect.x-350)/110)*-10
        self.plane_selector.rect.y = self.screen_size[1]-glm.abs(1-glm.abs(self.planes_buttons[id-1].rect.x-350)/110)*20

        for i in self.planes_buttons:
            i.update(glm.vec2(self.buttons_offset, int(i.plane_id == id)*y_pos))
            
    def render(self):
        self.surface.fill((3, 132, 252, 0))
        self.back_button.draw(self.surface)
        self.planes_panel.draw(self.surface)
        self.plane_selector.draw(self.surface)
        self.characteristics_panel.draw(self.surface)

        for i in self.planes_buttons:
            i.draw(self.surface)
        
        data = pygame.image.tostring(self.surface, "RGBA", True)
        self.texture.write(data)
        self.active = False

        self.texture.use(location=0)
        self.vao.render(moderngl.TRIANGLES)

    def check_event(self, event):
        self.back_button.handle_event(event)
        for i in self.planes_buttons:
            i.handle_event(event)