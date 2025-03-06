import glm
from .components.mesh import Mesh
from .components.transform import Transform


class GameObject:
    def __init__(self, app, components=None):
        if components == None:
            components = [Transform(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0), glm.vec3(1, 1, 1))]
        self.app = app
        self.ctx = app.ctx
        self.components = components
        self.transform = self.components[0]

    def update(self): 
        for i in self.components:
            if (isinstance(i, Mesh)):
                i.update(self.transform.m_model)
            else:
                i.update()

    def render(self):
        for i in filter(lambda x: isinstance(x, Mesh), self.components):
            i.render()

    def __repr__(self):
        return f'GameObject(components={self.components})'