from .components.transform import Transform
from .game_object import GameObject
import pygame
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

        self.rotation_speed = glm.vec3(0.01, 0.03, 0.03)
        self.speed = 0.5

        self.forward = glm.vec3(0)


    def update(self):
        super().update()
        
        self.forward.x = glm.cos(self.transform.rotation.y)
        self.forward.y = glm.sin(self.transform.rotation.z)
        self.forward.z = glm.sin(-self.transform.rotation.y)
        self.controll()
        self.follow_camera()

    def follow_camera(self):
        self.camera.position = self.transform.position + glm.vec3(self.forward.x, (-self.forward.y)/self.camera_offset.x, self.forward.z) * self.camera_offset.x + glm.vec3(0, self.camera_offset.y, 0)

    def controll(self):
        keys = pygame.key.get_pressed()

        self.horizontal = keys[pygame.K_a]-keys[pygame.K_d]
        self.vertical = keys[pygame.K_w]-keys[pygame.K_s]

        self.transform.rotation.x -= self.horizontal*self.rotation_speed.z

        if self.horizontal == 0.0:
            self.transform.rotation.x *= 0.95

        self.transform.rotation.z += self.vertical*self.rotation_speed.y
        
        if self.vertical == 0.0:
            self.transform.rotation.z *= 0.95

        self.transform.rotation.y -= glm.clamp(self.transform.rotation.x, -1.0, 1.0)*self.rotation_speed.x
        self.transform.rotation.z = glm.clamp(self.transform.rotation.z, -1.0, 1.0)
        self.transform.rotation.x = glm.clamp(self.transform.rotation.x, -1.0, 1.0)

        self.transform.position += self.forward*self.speed#*keys[pygame.K_SPACE]