import math

class Vector2Int:
    """
    A Vector2Int is a two-dimensional vector that stores two integers: x and y.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2Int(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2Int(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int):
        return Vector2Int(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: int):
        if scalar == 0:
            raise ValueError("Division by zero.")
        return Vector2Int(self.x / scalar, self.y / scalar)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return self.Magnitude() < other.Magnitude()

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}; {self.y})"
    
    def Magnitude(self):
        return math.hypot(self.x, self.y)
    
    def Normalized(self):
        if self.Magnitude() == 0: return Vector2Int(0, 0)
        else: return self / self.Magnitude()

    def Tuple(self):
        return (self.x, self.y)

    @classmethod
    def FromTuple(cls, tuple):
        return cls(tuple[0], tuple[1])
    
    @staticmethod
    def DotProduct(vectorA, vectorB):
        return vectorA.x * vectorB.x + vectorA.y * vectorB.y
    
    @staticmethod
    def Distance(vectorA, vectorB):
        return ((vectorA.x - vectorB.x) ** 2 + (vectorA.y - vectorB.y) ** 2) ** 0.5