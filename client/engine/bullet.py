import glm

from .components.mesh import Mesh
from .game_object import GameObject


class Bullet(GameObject):
    def __init__(self, app, components, speed):
        super().__init__(app, components)
        self.speed = speed

        self.components.append(
            Mesh(f"client/assets/objs/bullets/bullet.obj", self.app)
        )
        

        self.forward = glm.vec3(
            glm.cos(self.transform.rotation.y),
            glm.sin(self.transform.rotation.z),
            glm.sin(-self.transform.rotation.y)
        )
        self.tick = 0

    def distance(self, pos2):
        return glm.distance(self.transform.position, pos2)


    def update(self):
        self.tick += 1
        super().update()

        collision_1 = self.transform.position.y < 0 or self.transform.position.x < 0 or self.transform.position.x > 1000 or self.transform.position.z < 0 or self.transform.position.z > 1000 or self.transform.position.y > 200

        collision_2 = False

        for p in self.app.players.values():
            if glm.distance(self.transform.position, p.transform.position) < 20:
                collision_2 = True
                break


        if (collision_1 or collision_2) and self.tick > 100:
            self.app.bullets.remove(self)
            if collision_2:
                self.app.player.points+=1
                self.app.player.score+=5000

                p.__setattr__("game_over", True)
        

        self.transform.position += self.forward*self.speed