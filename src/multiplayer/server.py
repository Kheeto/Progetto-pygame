from core.gamemanager import GameManager
from core.singleton import Singleton
import socket
import threading
import json
import time

class Server(Singleton):
    """
    The Server is a Singleton class that manages the client connections and
    game state synchronization. This game is server authorative.
    """

    def __init__(self):
        super().__init__()
        self.clients = []
        self.lock = threading.Lock()
        self.TICK_RATE = 50
        self.BUFFER_SIZE = 4096
        self.socket = None
        self.game_state = None

        self.Start()

    def Start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', 12345))
        self.socket.listen()
        print("[SERVER] Listening on port 12345")

        threading.Thread(target=self.BroadcastGameState, daemon=True).start()

        while True:
            conn, addr = self.socket.accept()
            player_id = f"player{len(self.clients)+1}"
            with self.lock:
                self.clients.append((conn, player_id))
            threading.Thread(target=self.HandleClientConnection,
                             args=(conn, addr, player_id), daemon=True).start()
    
    def Stop(self):
        print("[SERVER] Shutting down...")
        with self.lock:
            for conn, _ in self.clients:
                try:
                    conn.close()
                except:
                    pass
            self.clients.clear()
        if self.socket:
            self.socket.close()

    def HandleClientConnection(self, conn, addr, player_id):
        conn.setblocking(False)
        print(f"[SERVER] Client {player_id} connected from {addr}")
        while True:
            try:
                data = conn.recv(self.BUFFER_SIZE)
                if data:
                    packet = json.loads(data.decode())
                    print(f"[SERVER] Received data from {player_id}: {packet}")
                time.sleep(0.01)
            except BlockingIOError:
                continue
            except (ConnectionResetError, json.JSONDecodeError):
                break

        with self.lock:
            self.clients.remove((conn, player_id))
        conn.close()
        print(f"Client {player_id} disconnected")

    def BroadcastGameState(self):
        self.game_state = GameManager.instance.GetGameState()

        while True:
            time.sleep(1 / self.TICK_RATE)
            with self.lock:
                state_packet = json.dumps({
                    "type": "game_state",
                    "timestamp": time.time(),
                    "game_state": self.game_state
                }).encode()

                for conn, _ in self.clients:
                    try:
                        conn.sendall(state_packet)
                    except:
                        continue
