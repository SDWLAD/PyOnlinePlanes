import glm
from .component import Component

class Transform(Component):
    def __init__(self, position, rotation, scale):
        super().__init__()
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.update_model()
    
    def update(self):
        self.update_model()

    def update_model(self):
        self.m_model = glm.mat4()
        self.m_model = glm.translate(self.m_model, self.position)
        self.m_model = glm.rotate(self.m_model, self.rotation.y, glm.vec3(0, 1, 0))
        self.m_model = glm.rotate(self.m_model, self.rotation.z, glm.vec3(0, 0, 1))
        self.m_model = glm.rotate(self.m_model, self.rotation.x, glm.vec3(1, 0, 0))
        self.m_model = glm.scale(self.m_model, self.scale)