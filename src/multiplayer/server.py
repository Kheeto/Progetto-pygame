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
        self.TICK_RATE = 20
        self.BUFFER_SIZE = 4096
        self.socket = None
        self.game_state = None

        threading.Thread(target=self.Start, daemon=True).start()

    def Start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', 12345))
        self.socket.listen()
        print("[SERVER] Listening on port 12345")

        threading.Thread(target=self.SendMessage, daemon=True).start()

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
                    if packet["type"] == "deploy_unit":
                        print("[SERVER] Received update from client")

                        card_id = packet["content"]["card_id"]
                        pos_x = packet["content"]["pos_x"]
                        pos_y = packet["content"]["pos_y"]
                        player_tag = packet["content"]["player_tag"]
                        enemy_tag = packet["content"]["enemy_tag"]

                        GameManager.instance.DeployCard(card_id, (pos_x, pos_y), player_tag, enemy_tag, False)
                else:
                    break # Disconnect
                time.sleep(0.01)
            except BlockingIOError:
                continue
            except (ConnectionResetError, ConnectionAbortedError, json.JSONDecodeError, OSError):
                break

        with self.lock:
            try:
                self.clients.remove((conn, player_id))
            except ValueError:
                pass
        conn.close()
        print(f"Client {player_id} disconnected")
    
    def SendMessage(self):
        while True:
            time.sleep(1 / self.TICK_RATE)

            with self.lock:
                content = None
                updates = GameManager.instance.updates
                if len(updates) > 0:
                    content = updates[0]
                    packet = json.dumps({
                        "type": "deploy_unit",
                        "content": content
                    }).encode()

                    for conn, _ in self.clients:
                        try:
                            print("[SERVER] Sent update to client")
                            conn.sendall(packet)
                            GameManager.instance.updates.pop(0)
                        except:
                            continue

    # def BroadcastGameState(self):
    #     while True:
    #         GameManager.instance.UpdateGameState()
    #         self.game_state = GameManager.instance.GetGameState()

    #         time.sleep(1 / self.TICK_RATE)
    #         with self.lock:
    #             state_packet = json.dumps({
    #                 "type": "game_state",
    #                 "game_state": self.game_state
    #             }).encode()

    #             for conn, _ in self.clients:
    #                 try:
    #                     conn.sendall(state_packet)
    #                 except:
    #                     continue
