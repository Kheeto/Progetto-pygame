from core.singleton import Singleton
from core.gamemanager import GameManager
import socket
import threading
import json
import time

class Client(Singleton):
    """
    The Client is a Singleton class that manages the server connection,
    updating the game state based on the received information.
    """

    def __init__(self, server_ip: str = 'localhost', server_port: int = 12345):
        super().__init__()
        self.BUFFER_SIZE = 4096
        self.TICK_RATE = 20
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self):
        try:
            self.socket.connect((self.SERVER_IP, self.SERVER_PORT))
            self.socket.setblocking(False)
            print(f"[CLIENT] Connected to server at {self.SERVER_IP}:{self.SERVER_PORT}")

            threading.Thread(target=self.ReceiveMessage, daemon=True).start()
            threading.Thread(target=self.SendMessage, daemon=True).start()
        except socket.error as e:
            print(f"[CLIENT] Error connecting to server: {e}")
    
    def Disconnect(self):
        try:
            self.socket.close()
            print("[CLIENT] Disconnected from server")
        except socket.error as e:
            print(f"[CLIENT] Error disconnecting: {e}")

    def SendMessage(self):
        while True:
            time.sleep(1 / self.TICK_RATE)

            updates = GameManager.instance.updates
            if len(updates) > 0:
                content = updates[0]
                packet = json.dumps({
                    "type": "deploy_unit",
                    "content": content
                }).encode()
                try:
                    print("[CLIENT] Sent update to server")
                    GameManager.instance.updates.pop(0)
                    self.socket.sendall(packet)
                except:
                    pass

    def ReceiveMessage(self):
        while True:
            try:
                data = self.socket.recv(self.BUFFER_SIZE)
                if data:
                    packet = json.loads(data.decode())
                    if packet["type"] == "deploy_unit":
                        print("[CLIENT] Received update from server")

                        card_id = packet["content"]["card_id"]
                        pos_x = packet["content"]["pos_x"]
                        pos_y = packet["content"]["pos_y"]
                        player_tag = packet["content"]["player_tag"]
                        enemy_tag = packet["content"]["enemy_tag"]

                        GameManager.instance.DeployCard(card_id, (pos_x, pos_y), player_tag, enemy_tag, False)
                    time.sleep(0.01)
                    return packet
            except BlockingIOError:
                continue
            except json.JSONDecodeError:
                continue
            time.sleep(0.01)