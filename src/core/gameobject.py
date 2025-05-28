from .vector2 import Vector2
from .singleton import Singleton
from .renderer import Renderer
import pygame

class GameObject:
    """
    A GameObject is a basic unique component of the game.
    """

    def __init__(self, id: int = -1, tags: list[str] = None, position: Vector2 = None, scale: Vector2 = None,
                 rotation: float = 0.0, color = (255, 255, 255), texture : pygame.Surface = None):
        self.id = id
        self.tags = tags if tags is not None else []
        self.position = position if position is not None else Vector2(0,0)
        self.scale = scale if scale is not None else Vector2(1,1)
        self.rotation = rotation
        self.color = color
        self.texture = texture

    def __repr__(self):
        return f"(GameObject #{self.id}, tags = {self.tags})"

    def Render(self):
        Renderer.instance.Render(self.position, self.scale, self.color, self.texture)

    def Update(self, dt: float):
        pass