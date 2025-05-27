from core.singleton import Singleton
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
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self):
        try:
            self.socket.connect((self.SERVER_IP, self.SERVER_PORT))
            self.socket.setblocking(False)
            print(f"[CLIENT] Connected to server at {self.SERVER_IP}:{self.SERVER_PORT}")

            threading.Thread(target=self.ReceiveMessage, daemon=True).start()
        except socket.error as e:
            print(f"[CLIENT] Error connecting to server: {e}")
    
    def Disconnect(self):
        try:
            self.socket.close()
            print("[CLIENT] Disconnected from server")
        except socket.error as e:
            print(f"[CLIENT] Error disconnecting: {e}")

    def SendMessage(self):
        packet = {
            "type": "deploy_unit",
            "unit": 1,
            "position": {"x": 10, "y": 10},
        }
        try:
            self.socket.sendall(json.dumps(packet).encode())
        except:
            pass

    def ReceiveMessage(self):
        while True:
            try:
                data = self.socket.recv(self.BUFFER_SIZE)
                if data:
                    packet = json.loads(data.decode())
                    if packet["type"] == "game_state":
                        print(f"Received state with {len(packet['game_state']['units'])} units")
                    time.sleep(0.01)
                    return packet
            except BlockingIOError:
                continue
            except json.JSONDecodeError:
                continue
            time.sleep(0.01)