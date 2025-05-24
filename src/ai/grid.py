import heapq
from core.vector2int import Vector2Int
from core.singleton import Singleton

DIRECTIONS =   [Vector2Int(1, 0), # Right
                Vector2Int(-1, 0), # Left
                Vector2Int(0, 1), # Down
                Vector2Int(0, -1), # Up
                Vector2Int(1, 1), # Down-Right
                Vector2Int(-1, 1), # Down-Left
                Vector2Int(1, -1), # Up-Right
                Vector2Int(-1, -1)] # Up-Left

class Grid(Singleton):
    """
    The Grid is the game arena that is made up of cells. A cell can be either walkable or blocked.
    It can be used to determine the shortest path ebtween two points using the A* algorithm.
    """

    def __init__(self, width, height, blocked_positions):
        super().__init__()
        self.width = width
        self.height = height
        self.walkable = [[True for _ in range(height)] for _ in range(width)]
        for pos in blocked_positions:
            self.walkable[pos.x][pos.y] = False

    def in_bounds(self, pos: Vector2Int):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def is_walkable(self, pos: Vector2Int):
        return self.in_bounds(pos) and self.walkable[pos.x][pos.y]

    def get_neighbors(self, pos: Vector2Int):
        return [pos + d for d in DIRECTIONS if self.is_walkable(pos + d)]

    # A* pathfinding algorithm
    def find_path(self, start: Vector2Int, goal: Vector2Int):
        open_set = []
        heapq.heappush(open_set, (0, start))
        previous_node = {}
        g = {start: 0}
        f = {start: Vector2Int.Distance(start, goal)}

        while open_set:
            _, node = heapq.heappop(open_set)

            # The path has been found
            if node == goal:
                path = []
                while node in previous_node:
                    path.append(node)
                    node = previous_node[node]
                path.append(start)
                path.reverse()
                return path

            for other in self.get_neighbors(node):
                new_g = g[node] + 1
                if other not in g or new_g < g[other]:
                    previous_node[other] = node
                    g[other] = new_g
                    f[other] = new_g + Vector2Int.Distance(other, goal)
                    heapq.heappush(open_set, (f[other], other))

        return [] # No path found