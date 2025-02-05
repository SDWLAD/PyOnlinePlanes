import pygame
import moderngl
import numpy as np

class Client:
    def __init__(self, width=800, height=600, title="PyOnlinePlanes"):
        pygame.init()
        pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(title)
        self.ctx = moderngl.create_context()
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.ctx.clear(0.1, 0.1, 0.1)

if __name__ == "__main__":
    client = Client()
    client.run()