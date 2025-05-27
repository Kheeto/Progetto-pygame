from core import *
import pygame

class Explosion(GameObject):
    def __init__(self, id: int = -1, tags: list[str] = [], position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1),
                 rotation: float = 0.0, color = (255, 255, 255), texture : pygame.Surface = None):
        super().__init__(id,tags,position,scale,rotation,color,texture)

        self.timer = 0.0
        self.frame_duration = 0.03
        self.frame = 0
        self.duration = 2.1

        self.animation = [ pygame.image.load(f'src/img/explosion/frame00{i:02}.png').convert_alpha() for i in range(0, 70+1) ]
    
    def Render(self):
        self.frame = self.timer // self.frame_duration
        if self.frame > 70:
            return
        
        self.texture = self.animation[round(self.frame)]
        Renderer.instance.Render(self.position, self.scale, self.color, self.texture)

    def Update(self, dt: float):
        self.timer += dt

        if self.timer >= self.duration:
            GameObjectManager.instance.delQueue.append(self)