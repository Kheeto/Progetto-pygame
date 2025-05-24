from core.vector2 import Vector2
from core.vector2int import Vector2Int
from ai.grid import Grid

class Agent:
    """
    An Agent is an entity that navigates the grid by costantly moving towards its target.
    """
    def __init__(self, position: Vector2, target: Vector2):
        self.id = id
        self.position = position
        self.target = target
    
    def UpdatePosition(self, position: Vector2):
        self.position = position
    
    def UpdateTarget(self, target: Vector2):
        self.target = target

    def GetDirection(self) -> Vector2:
        if not Grid.instance:
            return None
        if not self.target:
            return None

        positionInt = Vector2Int(int(round(self.position.x)), int(round(self.position.y)))
        targetInt = Vector2Int(int(round(self.target.x)), int(round(self.target.y)))
        path = Grid.instance.find_path(positionInt , targetInt)
        if not path or path == []:
            return None
        
        direction = (Vector2.FromTuple(path[1]) - self.position).Normalized()
        return direction