from core import *
from characters.character import Character
from characters.castle import Castle
from characters.health import Health
from ai.grid import Grid
import pygame

class Explosion(GameObject):
    def __init__(self, id: int = -1, tags: list[str] = [], position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1),
                 rotation: float = 0.0, color = (255, 255, 255), texture : pygame.Surface = None, targetTags : list[str] = None):
        super().__init__(id,tags,position,scale,rotation,color,texture)

        self.timer = 0.0
        self.frame_duration = 0.02
        self.frame = 0
        self.duration = 1.4

        self.animation = [ pygame.image.load(f'src/img/explosion/frame00{i:02}.png').convert_alpha() for i in range(0, 70+1) ]
        self.exploded = False
        self.damage = 120
        self.range = 2

        self.targetTags = targetTags if targetTags is not None else []
    
    def Render(self):
        self.frame = self.timer // self.frame_duration
        if self.frame > 70:
            return
        
        self.texture = self.animation[round(self.frame)]
        Renderer.instance.Render(self.position, self.scale, self.color, self.texture)
    
    def GetDamage(self, distance):
        return round(-float(self.damage)/float(self.range)*distance + self.damage)

    def Update(self, dt: float):
        self.timer += dt

        if not self.exploded:
            self.exploded = True
            # Check for damaged characters        
            for gameobject in GameObjectManager.instance.GetAllGameObjects():
                if gameobject.id == self.id:
                    continue
                else:
                    distance = Vector2.Distance(self.position, gameobject.position)
                    if distance < self.range:
                        if isinstance(gameobject, Character) and gameobject.tags == self.targetTags:
                            gameobject.health.take_damage(self.GetDamage(distance))
            # Check if castle was damaged
            # for i, position in enumerate(Grid.instance.blocked_positions, 80):
            #     if 80 <= i <= 131: # Left castle
            #         distance = Vector2.Distance(self.position, position)
            #         if distance < self.range:
            #             GameObjectManager.instance.GetGameObjectById(10).health.take_damage(self.damage)
            #             break
            #     elif i > 131:
            #         distance = Vector2.Distance(self.position, position)
            #         if distance < self.range:
            #             GameObjectManager.instance.GetGameObjectById(11).health.take_damage(self.damage)
            #             break

        if self.timer >= self.duration:
            GameObjectManager.instance.delQueue.append(self)