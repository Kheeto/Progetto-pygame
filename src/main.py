import pygame
import sys
from core import *
from ai import *
from characters import *
from menu import *
from multiplayer import *

pygame.init()

FPS = 60
UNIT_SCALE = 10
CAMERA_SPEED = 1
ZOOM_SPEED = 1.1

screen = pygame.display.set_mode((1188, 737+50))
pygame.display.set_caption("Gioco fighissimo")

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)

pygame.mixer.init()
pygame.mixer.music.load("src/audio/song.mp3")
pygame.mixer.music.play(-1) # Loop

menu = MainMenu(screen)

camera_pos = Vector2(0, 0)

gameObjectManager = GameObjectManager()
gameManager = GameManager()

arena = GameObject(
    id=2,
    position=Vector2(0, 0),
    scale=Vector2(29, 18),
    texture=pygame.image.load("src/img/Background.png").convert_alpha()
)
castle1 = Castle(
    id=10,
    tags=["blue", "building"],
    position=Vector2(5, 8.5),
    healthPosition=Vector2(2, 8.5)
)
castle2 = Castle(
    id=11,
    tags=["red", "building"],
    position=Vector2(23, 8.5),
    healthPosition=Vector2(26, 8.5)
)

GameObjectManager.instance.AddGameObject(arena)
GameObjectManager.instance.AddGameObject(castle1)
GameObjectManager.instance.AddGameObject(castle2)

renderer = Renderer(camera_pos, UNIT_SCALE, screen)

blocked_positions = [
    # Water
    Vector2(12,0), Vector2(13,0), Vector2(14,0), Vector2(15,0), Vector2(16,0),
    Vector2(12,1), Vector2(13,1), Vector2(14,1), Vector2(15,1), Vector2(16,1),
    Vector2(12,2), Vector2(13,2), Vector2(14,2), Vector2(15,2), Vector2(16,2),
    Vector2(12,4), Vector2(13,4), Vector2(14,4), Vector2(15,4), Vector2(16,4),
    Vector2(12,5), Vector2(13,5), Vector2(14,5), Vector2(15,5), Vector2(16,5),
    Vector2(12,6), Vector2(13,6), Vector2(14,6), Vector2(15,6), Vector2(16,6),
    Vector2(12,7), Vector2(13,7), Vector2(14,7), Vector2(15,7), Vector2(16,7),
    Vector2(12,8), Vector2(13,8), Vector2(14,8), Vector2(15,8), Vector2(16,8),
    Vector2(12,9), Vector2(13,9), Vector2(14,9), Vector2(15,9), Vector2(16,9),
    Vector2(12,10), Vector2(13,10), Vector2(14,10), Vector2(15,10), Vector2(16,10),
    Vector2(12,11), Vector2(13,11), Vector2(14,11), Vector2(15,11), Vector2(16,11),
    Vector2(12,12), Vector2(13,12), Vector2(14,12), Vector2(15,12), Vector2(16,12),
    Vector2(12,13), Vector2(13,13), Vector2(14,13), Vector2(15,13), Vector2(16,13),
    Vector2(12,15), Vector2(13,15), Vector2(14,15), Vector2(15,15), Vector2(16,15),
    Vector2(12,16), Vector2(13,16), Vector2(14,16), Vector2(15,16), Vector2(16,16),
    Vector2(12,17), Vector2(13,17), Vector2(14,17), Vector2(15,17), Vector2(16,17),

    # Left castle
    Vector2(0,3), Vector2(0,4), Vector2(0,5), Vector2(0,6), Vector2(0,7),
    Vector2(0,8), Vector2(0,9), Vector2(0,10), Vector2(0,11), Vector2(0,12),
    Vector2(0,13), Vector2(0,14),
    Vector2(1,3), Vector2(1,4), Vector2(1,5), Vector2(1,6), Vector2(1,7),
    Vector2(1,8), Vector2(1,9), Vector2(1,10), Vector2(1,11), Vector2(1,12),
    Vector2(1,13), Vector2(1,14),
    Vector2(2,3), Vector2(2,4), Vector2(2,5), Vector2(2,6), Vector2(2,7),
    Vector2(2,8), Vector2(2,9), Vector2(2,10), Vector2(2,11), Vector2(2,12),
    Vector2(2,13), Vector2(2,14),
    Vector2(3,3), Vector2(3,4), Vector2(3,5), Vector2(3,6), Vector2(3,7),
    Vector2(3,8), Vector2(3,9), Vector2(3,10), Vector2(3,11), Vector2(3,12),
    Vector2(3,13), Vector2(3,14),
    Vector2(4,7), Vector2(4,8), Vector2(4,9), Vector2(4,10),

    # Right castle
    Vector2(28,3), Vector2(28,4), Vector2(28,5), Vector2(28,6), Vector2(28,7),
    Vector2(28,8), Vector2(28,9), Vector2(28,10), Vector2(28,11), Vector2(28,12),
    Vector2(28,13), Vector2(28,14),
    Vector2(27,3), Vector2(27,4), Vector2(27,5), Vector2(27,6), Vector2(27,7),
    Vector2(27,8), Vector2(27,9), Vector2(27,10), Vector2(27,11), Vector2(27,12),
    Vector2(27,13), Vector2(27,14),
    Vector2(26,3), Vector2(26,4), Vector2(26,5), Vector2(26,6), Vector2(26,7),
    Vector2(26,8), Vector2(26,9), Vector2(26,10), Vector2(26,11), Vector2(26,12),
    Vector2(26,13), Vector2(26,14),
    Vector2(25,3), Vector2(25,4), Vector2(25,5), Vector2(25,6), Vector2(25,7),
    Vector2(25,8), Vector2(25,9), Vector2(25,10), Vector2(25,11), Vector2(25,12),
    Vector2(25,13), Vector2(25,14),
    Vector2(24,7), Vector2(24,8), Vector2(24,9), Vector2(24,10),
]

grid = Grid(29, 18, blocked_positions)

menu_active = True

while True:
    screen.fill((30, 30, 30))
    screen_size = Vector2.FromTuple(screen.get_size())

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if menu_active:
            menu.handle_event(event)
    
    if menu_active:
        menu.update()
        menu.render()

    if menu.next_screen == "host":
        print("Hai cliccato HOST")
        menu_active = False
        menu.next_screen = None
    elif menu.next_screen == "join":
        print("Hai cliccato JOIN")
        menu_active = False
        menu.next_screen = None

    if menu_active:
        clock.tick(FPS)
        pygame.display.flip()
        continue

    dt = clock.tick(FPS) / 1000

    if not menu_active:
        GameObjectManager.instance.Update(dt)

    cards.Update(screen, events, dt)

    pygame.display.flip()