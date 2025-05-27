from ai.agent import Agent
from core.gameobject import GameObject
from core.gameobjectmanager import GameObjectManager
from core.vector2 import Vector2

class Character(GameObject):
    def __init__(self, id: int = -1, tags: list[str] = [], position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1),
                 rotation: float = 0.0,color = (255, 255, 255), agent: Agent = None, speed = float(1), targetTags : list[str] = []):
        super().__init__(id=id, tags=tags, position=position, scale=scale, rotation=rotation, color=color)
        self.agent = agent
        self.speed = speed
        self.targetTags = targetTags
        self.currentTarget = None
        self.direction = None

    def Update(self, dt: float):
        self.agent.UpdatePosition(self.position)

        self.direction = self.agent.GetDirection()
        if self.direction is not None:
          self.position += self.direction * self.speed * dt

        # Find a new target
        if self.currentTarget is None:
          targets = GameObjectManager.instance.GetGameObjectsByTagsAll(self.targetTags)
          closestTarget = GameObjectManager.instance.GetGameObjectById(targets[0]) if targets else None
          if closestTarget is not None:
            for target in targets:
              targetObject = GameObjectManager.instance.GetGameObjectById(target)
              if Vector2.Distance(self.position, targetObject.position) < Vector2.Distance(self.position, closestTarget.position):
                  closestTarget = targetObject
            self.currentTarget = closestTarget

        if self.currentTarget is None:
            return
        
        self.agent.UpdateTarget(self.currentTarget.position)