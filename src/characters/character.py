from ai.agent import Agent
from core.gameobject import GameObject
from core.gameobjectmanager import GameObjectManager
from core.vector2 import Vector2
from characters.health import Health
from core.renderer import Renderer

class Character(GameObject):
    def __init__(self, id: int = -1, tags: list[str] = None, position: Vector2 = None, scale: Vector2 = None,
                 rotation: float = 0.0, color = (255, 255, 255), agent: Agent = None, speed : float = 1.0, targetTags : list[str] = None,
                 maxHealth : float = 100):
        super().__init__(id=id, tags=tags, position=position, scale=scale, rotation=rotation, color=color)
        self.agent = agent if agent is not None else Agent()
        self.speed = speed
        self.targetTags = targetTags if targetTags is not None else []
        self.currentTarget = None
        self.direction = None
        self.health = Health(self.position + Vector2(0, 1.5), maxHealth)

    def Update(self, dt: float):
        self.agent.UpdatePosition(self.position)

        self.direction = self.agent.GetDirection()
        if self.direction is not None:
          self.position += self.direction * self.speed * dt

        self.LookForTargets()

        self.health.position = self.position + Vector2(0, 1.5)
        if self.health.current_life <= 0:
           # Dead
           GameObjectManager.instance.delQueue.append(self.character)

    def LookForTargets(self):
        if self.currentTarget is None or GameObjectManager.instance.GetGameObjectById(self.currentTarget.id) is None:
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
    
    def Render(self):
       self.health.Render()
       super().Render()
    
    @property
    def center(self):
        return Vector2(self.position + self.scale / 2)