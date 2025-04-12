import pygame
from utils.singleton import Singleton

class SoundController(metaclass=Singleton):
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = {}

    def load_sound(self, name, filepath): self.sounds[name] = pygame.mixer.Sound(filepath)
    def play_sound(self, name): self.sounds[name].play()
    def stop_sound(self, name): self.sounds[name].stop()

    def load_music(self, name, filepath): self.music[name] = pygame.mixer.Sound(filepath)
    def set_music_volume(self, name, volume): self.music[name].set_volume(volume)
    def play_music(self, name, loops): self.music[name].play(loops)
    def stop_music(self, name): self.music[name].stop()

    def stop_all(self): pygame.mixer.stop()