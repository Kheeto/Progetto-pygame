from core.singleton import Singleton

class GameManager(Singleton):
    """
    The GameManager is a Singleton class that manages the game state, which includes
    all of the information that is shared between the server and the client.
    """

    def __init__(self):
        super().__init__()
        self.game_state = {}

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