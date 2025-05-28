from core.gameobject import GameObject
from core.gameobjectmanager import GameObjectManager
from core.vector2 import Vector2
from core.renderer import Renderer
from characters.character import Character
from characters.castle import Castle
import pygame
import math

class Projectile(GameObject):
    def __init__(self, id: int = -1, tags: list[str] = [], position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1),
                 rotation: float = 0.0, color = (255, 255, 255), texture : pygame.Surface = None, direction : Vector2 = Vector2(1,1),
                 speed : float = 2, damage : int = 20, targetTags : list[str] = None):
        super().__init__(id, tags, position, scale, rotation, color, texture)

        self.rotation = math.degrees(math.atan2(direction.y, direction.x))
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.targetTags = targetTags if targetTags is not None else []
    
    def Render(self):
        Renderer.instance.Render(self.position, self.scale, self.color, pygame.transform.rotate(self.texture, self.rotation))
    
    def Update(self, dt):
        self.position += self.direction * self.speed * dt

        # Check for collision        
        for gameobject in GameObjectManager.instance.GetAllGameObjects():
            if gameobject.id == self.id:
                continue
            else:
                if Vector2.Distance(self.position, gameobject.position) < 0.5:
                    GameObjectManager.instance.delQueue.append(self)
                    if (isinstance(gameobject, Character) or isinstance(gameobject, Castle)) and gameobject.tags == self.targetTags:
                        gameobject.health.take_damage(self.damage)