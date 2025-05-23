import math

class Vector2:
    """
    A Vector2 is a two-dimensional vector that stores two floating point numbers: x and y.
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        if scalar == 0:
            raise ValueError("Division by zero.")
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return self.Magnitude < other.Magnitude()

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}; {self.y})"
    
    def Magnitude(self):
        return math.hypot(self.x, self.y)
    
    def Normalized(self):
        if self.Magnitude() == 0: return Vector2(0, 0)
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