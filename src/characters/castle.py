from core.gameobject import GameObject
from core.vector2 import Vector2
from characters.health import Health

class Castle(GameObject):
    def __init__(self, id: int = -1, tags : list[str] = [], position: Vector2 = Vector2(0, 0), healthPosition : Vector2 = Vector2(0,0)):
        super().__init__(id, tags, position, Vector2(1, 1), 0, (255, 255, 255), None)

        self.health = Health(healthPosition, 1000)
    
    def Render(self):
        self.health.Render()

    def Update(self, dt: float):
        if self.health.current_life <= 0:
            # Destroyed
            pass