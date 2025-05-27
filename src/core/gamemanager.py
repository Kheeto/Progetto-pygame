from core import *
from characters import *
from ai import *
import copy

class GameManager(Singleton):
    """
    The GameManager is a Singleton class that manages the game state, which includes
    all of the information that is shared between the server and the client.
    """

    def __init__(self):
        super().__init__()
        self.game_state = {}
        self.prefabs = None
    
    def DeployCard(self, card_id, mouse_pos):
        spawn_position = Renderer.pixels_to_units(Renderer.instance, Vector2.FromTuple(mouse_pos))

        if self.prefabs is None: self.InitializePrefabs()
        prefab = self.prefabs[card_id]

        # Spawn 3 goblins(es)
        if card_id == 2:
            id = GameObjectManager.instance.AddGameObject(copy.copy(prefab))
            GameObjectManager.instance.GetGameObjectById(id).position = spawn_position + Vector2(13.0, 8.0)
            id = GameObjectManager.instance.AddGameObject(copy.copy(prefab))
            GameObjectManager.instance.GetGameObjectById(id).position = spawn_position + Vector2(14.0, 8.0)
            id = GameObjectManager.instance.AddGameObject(copy.copy(prefab))
            GameObjectManager.instance.GetGameObjectById(id).position = spawn_position + Vector2(13.5, 9.0)

        else:
            id = GameObjectManager.instance.AddGameObject(copy.copy(prefab))
            GameObjectManager.instance.GetGameObjectById(id).position = spawn_position + Vector2(13.5, 8.0)

    def UpdateGameState(self):
        self.game_state = {
            "units": [
                {
                    "id": 1,
                    "position": {"x": 10, "y": 10},
                    "texture": "unit_texture.png"
                }
            ]
        }
        pass

    def GetGameState(self):
        return self.game_state
    
    def InitializePrefabs(self):
        self.prefabs = {
            0: Dwarf(
                id=-1,
                tags=["blue"],
                scale=Vector2(2,2),
                agent=Agent(),
                targetTags=["red"]
            ),
            1: Elf(
                id=-1,
                tags=["red"],
                scale=Vector2(2,2),
                agent=Agent(),
                speed=0.7,
                targetTags=["blue"],
            ),
            2: Goblin(
                id=-1,
                tags=["red"],
                scale=Vector2(1.35,1.35),
                agent=Agent(),
                speed=1.05,
                targetTags=["blue"],
            ),
            3: Explosion(
                id=-1,
                scale=Vector2(2.5,2.5)
            )
        }