from multiplayer import *
import time

client = Client("localhost", 12345)

client.Connect()

for _ in range(3):
    client.SendMessage()
    message = client.ReceiveMessage()
    print(f"Received message: {message}")
    time.sleep(3)

client.Disconnect()