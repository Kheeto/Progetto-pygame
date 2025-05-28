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
        self.updates = []

        self.player_tag = None
        self.enemy_tag = None
    
    def DeployCard(self, card_id, mouse_pos, player_tag, enemy_tag, send_on_network):
        if send_on_network:
            self.updates.append({"card_id": card_id, "pos_x": mouse_pos[0], "pos_y": mouse_pos[1], "player_tag": player_tag, "enemy_tag": enemy_tag})

        spawn_position = Renderer.pixels_to_units(Renderer.instance, Vector2.FromTuple(mouse_pos))

        if self.prefabs is None: self.InitializePrefabs()
        prefab = self.prefabs[card_id]

        # Spawn 3 goblins(es)
        if card_id == 2:
            copy_1 = copy.copy(prefab)
            copy_1.tags = [player_tag]
            copy_1.targetTags = [enemy_tag]
            copy_1.health = Health(None, 40)
            copy_1.position = spawn_position + Vector2(13.0, 8.0)
            GameObjectManager.instance.addQueue.append(copy_1)
            copy_2 = copy.copy(prefab)
            copy_2.tags = [player_tag]
            copy_2.targetTags = [enemy_tag]
            copy_2.health = Health(None, 40)
            copy_2.position = spawn_position + Vector2(14.0, 8.0)
            GameObjectManager.instance.addQueue.append(copy_2)
            copy_3 = copy.copy(prefab)
            copy_3.tags = [player_tag]
            copy_3.targetTags = [enemy_tag]
            copy_3.health = Health(None, 40)
            copy_3.position = spawn_position + Vector2(13.5, 9.0)

        else:
            copy_prefab = copy.copy(prefab)
            copy_prefab.tags = [player_tag]
            copy_prefab.targetTags = [enemy_tag]
            copy_prefab.position = spawn_position + Vector2(13.5, 8.0)

            if card_id != 2:
                copy_prefab.health = Health(None, 100)

            GameObjectManager.instance.addQueue.append(copy_prefab)

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
                tags=[],
                scale=Vector2(2,2),
                agent=Agent(),
                targetTags=[]
            ),
            1: Elf(
                id=-1,
                tags=[],
                scale=Vector2(2,2),
                agent=Agent(),
                speed=0.7,
                targetTags=[],
            ),
            2: Goblin(
                id=-1,
                tags=[],
                scale=Vector2(1.35,1.35),
                agent=Agent(),
                speed=1.05,
                targetTags=[],
            ),
            3: Explosion(
                id=-1,
                scale=Vector2(2.7,2.7)
            )
        }