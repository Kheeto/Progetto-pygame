from ai.agent import Agent
from core.gameobject import GameObject
from core.vector2 import Vector2

class Character(GameObject):
    def __init__(self, id: int = -1, tags: list[str] = [], position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1), rotation: float = 0.0, color = (255, 255, 255), agent: Agent = None, speed = float(1)):
        super().__init__(id=id, tags=tags, position=position, scale=scale, rotation=rotation, color=color)
        self.agent = agent
        self.speed = speed

    def Update(self, dt: float):
        self.agent.UpdatePosition(self.position)
        self.agent.UpdateTarget(Vector2(20,20))
        direction = self.agent.GetDirection()
        if direction is None:
          return

        self.position += direction * self.speed