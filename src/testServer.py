from multiplayer import *
from core import *

gamemanager = GameManager()

server = Server()
server.BroadcastGameState()