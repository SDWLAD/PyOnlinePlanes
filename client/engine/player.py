from .components.transform import Transform
from .game_object import GameObject
import glm


class Player(GameObject):
    def __init__(self, scene, components=None):
        if components is None:
            components = [Transform(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0), glm.vec3(1, 1, 1))]
        super().__init__(scene, components)

        self.scene = scene
        self.camera = scene.camera
        self.camera.target = self.transform.position
        self.camera_offset = glm.vec3(-15, 4, 0)

        self.forward = glm.vec3(0)


    def update(self):
        super().update()
        self.follow_camera()

    def follow_camera(self):
        self.camera.position = self.transform.position - self.camera_offset