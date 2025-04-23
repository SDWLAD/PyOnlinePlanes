from .animator import Animation
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

        self.hitbox = scene.app.selected_plane["hitbox"]
        self.speed = scene.app.selected_plane["speed"]
        self.rotation_speed = glm.vec3(0.01, 0.03, 0.03)

        self.forward = glm.vec3(0)

        self.camera_start_animation = Animation([(0, glm.vec3(0, 1, 0)), (2, glm.vec3(-15, 4, 0))], "ease_out_cubic")
        self.camera_start_animation.active = True
        self.game_over_animation = Animation([(0, glm.vec3(15, 4, 0)), (0.5, glm.vec3(30, 30, 0)), (5, glm.vec3(35, 35, 0)), (5, lambda: self.app.app.change_scene("game_over", 
            int(self.distance)
        ))], "ease_out_expo")
        
        self.distance = 0.0

    def update(self, terrain):
        super().update()
        self.camera_start_animation.update()
        self.game_over_animation.update()

        self.forward.x = glm.cos(self.transform.rotation.y)
        self.forward.y = glm.sin(self.transform.rotation.z)
        self.forward.z = glm.sin(-self.transform.rotation.y)
        
        if not self.game_over_animation.active: self.controll()
        if terrain != None: self.collision_detect(terrain.terrain)

        self.follow_camera()

    def follow_camera(self):
        if self.camera_start_animation.active: self.camera_offset = self.camera_start_animation.get_value()
        if self.game_over_animation.active: self.camera_offset = self.game_over_animation.get_value()

        self.camera.position = self.transform.position + glm.vec3(self.forward.x, (-self.forward.y)/self.camera_offset.x, self.forward.z) * self.camera_offset.x + glm.vec3(0, self.camera_offset.y, 0)

    def collision_detect(self, terrain):
        player_pos = self.transform.position
        player_pos.x = glm.clamp(player_pos.x, 10, 990)
        player_pos.y = glm.clamp(player_pos.y, 0, 200)
        player_pos.z = glm.clamp(player_pos.z, 10, 990)

        bottom = (player_pos.y+self.hitbox[0]) <= terrain[int(player_pos.x + self.transform.rotation.x * self.hitbox[2]), int(player_pos.z + self.transform.rotation.z * self.hitbox[3])]
        right = (player_pos.y+self.hitbox[0]) <= terrain[int(player_pos.x + self.transform.rotation.x * self.hitbox[2] + self.transform.rotation.z * self.hitbox[4]), int(player_pos.z + self.transform.rotation.x * self.hitbox[4] - self.transform.rotation.z * self.hitbox[2])]
        left = (player_pos.y+self.hitbox[0]) <= terrain[int(player_pos.x + self.transform.rotation.x * self.hitbox[3] - self.transform.rotation.z * self.hitbox[4]), int(player_pos.z + self.transform.rotation.x * self.hitbox[4] + self.transform.rotation.z * self.hitbox[3])]
        front = (player_pos.y+self.hitbox[0]) <= terrain[int(player_pos.x + self.transform.rotation.x * self.hitbox[4]), int(player_pos.z + self.transform.rotation.z * self.hitbox[4])]
        back = (player_pos.y+self.hitbox[0]) <= terrain[int(player_pos.x + self.transform.rotation.x * self.hitbox[5]), int(player_pos.z + self.transform.rotation.z * self.hitbox[5])]


        if True in [bottom, right, left, front, back]:
            self.game_over_animation.active=True

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
        self.distance += self.speed