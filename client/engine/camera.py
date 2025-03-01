from settings import *
import glm

class Camera:
    def __init__(self, app):
        self.position = glm.vec3(-10, 42, 0)
        self.rotation = glm.vec2(0, 0)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.target = self.forward

        self.m_proj = glm.perspective(glm.radians(50), app.settings.window_size[0]/app.settings.window_size[1], 0.1, app.settings.distance_of_view)
        self.m_view = glm.mat4()

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.target, self.up)

    def update_vectors(self):
        self.rotation.y = glm.clamp(self.rotation.y, -glm.radians(89), glm.radians(89))

        self.forward.x = glm.cos(self.rotation.x) * glm.cos(self.rotation.y)
        self.forward.y = glm.sin(self.rotation.y)
        self.forward.z = glm.sin(self.rotation.x) * glm.cos(self.rotation.y)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))