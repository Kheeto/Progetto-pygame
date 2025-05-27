import pygame
from core.gameobjectmanager import GameObjectManager
from core.renderer import Renderer
from core.vector2 import Vector2

def get_perc(x, tot):
    return max(0, min(1, x / tot))

class Health:
    def __init__(self, position, life):
        self.position = position
        self.current_life = self.tot_life = life

    def take_damage(self, damage):
        self.current_life -= damage

    def Render(self):
        bar_width = 1
        bar_height = .16
        Renderer.instance.Render(self.position, Vector2(bar_width * self.current_life / self.tot_life, bar_height), (200,0,0)) # Green bar
        Renderer.instance.Render(self.position, Vector2(bar_width, bar_height), (0,200,0)) # Red background
        #Renderer.instance.Render(self.position, Vector2(bar_width * self.current_life / self.tot_life, bar_height), (200,0,0)) # Green bar