from .singleton import Singleton
from .gameobject import GameObject
import random
import time

class GameObjectManager(Singleton):
    """
    The GameObjectManager is a Singleton class that manages the constant update of game objects, as well as their creation and destruction.
    """

    def __init__(self, gameObjects: dict[int, GameObject] = {}, gameObjectsByTag: dict[str, list[int]] = {}):
        super().__init__()

        self.gameObjects = gameObjects
        self.gameObjectsByTag = gameObjectsByTag

    def Update(self, delta_time: float):
        for gameObject in self.gameObjects.values():
            gameObject.Update(delta_time)
            gameObject.Render()

    def AddGameObject(self, gameObject: GameObject):
        if gameObject.id is None or gameObject.id == -1:
            gameObject.id = random.randint(0, 2**31 - 1)
            while self.gameObjects.get(gameObject.id) is not None:
                gameObject.id = random.randint(0, 2**31 - 1)
            return self.AddGameObject(gameObject)
        elif gameObject.id not in self.gameObjects:
            self.gameObjects[gameObject.id] = gameObject

            for tag in gameObject.tags:
                if tag not in self.gameObjectsByTag:
                    self.gameObjectsByTag[tag] = []
                self.gameObjectsByTag[tag].append(gameObject.id)

            return gameObject.id
        else:
            raise ValueError(f"GameObject with id {gameObject.id} already exists.")
    
    def RemoveGameObject(self, id: int):
        if id in self.gameObjects:
            gameObject = self.gameObjects[id]
            del self.gameObjects[id]

            for tag in gameObject.tags:
                if tag in self.gameObjectsByTag and id in self.gameObjectsByTag[tag]:
                    self.gameObjectsByTag[tag].remove(id)
                    if not self.gameObjectsByTag[tag]:
                        del self.gameObjectsByTag[tag]
        else:
            raise ValueError(f"GameObject with id {id} does not exist.")
    
    def GetGameObjectById(self, id: int) -> GameObject:
        return self.gameObjects[id] if id in self.gameObjects else None
    
    def GetGameObjectsByTag(self, tag: str) -> list[GameObject]:
        return self.gameObjectsByTag[tag] if tag in self.gameObjectsByTag else []
    
    def GetGameObjectsByTagsAll(self, tags: list[str]) -> list[GameObject]:
        """
        Returns a list of game objects that have ALL the specified tags.
        """
        gameObjects = []
        for tag in tags:
            if tag in self.gameObjectsByTag:
                gameObjects.extend(self.gameObjectsByTag[tag])
        
        return list(set(gameObjects))
    
    def GetGameObjectsByTags(self, tags: list[str]) -> list[GameObject]:
        """
        Returns a list of game objects that have at least ONE of the specified tags.
        """
        gameObjects = []
        for tag in tags:
            if tag in self.gameObjectsByTag:
                gameObjects.extend(self.gameObjectsByTag[tag])
        
        return list(set(gameObjects))
    
    def GetAllGameObjects(self) -> list[GameObject]:
        return list(self.gameObjects.values())