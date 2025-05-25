import pygame
from characters.character import Character
from core import *

class Tormex(Character):
    def __init__(self, agent = None, speed = 0):
        super().__init__(agent, speed)
        self.life = 100 # da modificare
        self.size = Vector2(123,123)
        
        self.img = pygame.surface.Surface(self.size.Tuple())
        self.img.fill('White')
        self.rect = self.img.get_rect()

        self.rect.center = Vector2(123,123).Tuple()