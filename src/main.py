import pygame
import sys
from core import *
from ai import *
from characters.character import *

pygame.init()

FPS = 60
UNIT_SCALE = 10
CAMERA_SPEED = 1
ZOOM_SPEED = 1.1

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Gioco fighissimo")
clock = pygame.time.Clock()

camera_pos = Vector2(0, 0)

# Background setting


gameObjectManager = GameObjectManager()
gameObjectManager.AddGameObject(
    Character(
        id=1,
        position=Vector2(10,10),
        scale=Vector2(2,2),
        color=(0,200,0),
        agent = Agent(
            position=Vector2(10,10),
            target=Vector2(20,20)
        ),
        speed=1
    )
)

renderer = Renderer(camera_pos, UNIT_SCALE, screen)

grid = Grid(45, 20, [])

while True:
    screen_size = Vector2.FromTuple(screen.get_size())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Zoom
        elif event.type == pygame.MOUSEWHEEL:
            screen_center = screen_size / 2
            world_pos = camera_pos

            old_scale = renderer.unit_scale
            if event.y > 0:
                renderer.unit_scale *= ZOOM_SPEED
            elif event.y < 0:
                renderer.unit_scale /= ZOOM_SPEED

            ratio = old_scale / renderer.unit_scale

            camera_pos.x = world_pos.x + (screen_center.x - screen_center.x) / renderer.unit_scale * (1 - ratio)
            camera_pos.y = world_pos.y - (screen_center.y - screen_center.y) / renderer.unit_scale * (1 - ratio)

    # Input
    keys = pygame.key.get_pressed()
    delta = CAMERA_SPEED / renderer.unit_scale
    if keys[pygame.K_LEFT]:
        camera_pos.x -= delta
    if keys[pygame.K_RIGHT]:
        camera_pos.x += delta
    if keys[pygame.K_UP]:
        camera_pos.y += delta
    if keys[pygame.K_DOWN]:
        camera_pos.y -= delta

    screen_size = Vector2.FromTuple(screen.get_size())
    screen.fill((30, 30, 30))

    gameObjectManager.Update(1 / FPS)

    pygame.display.flip()
    clock.tick(FPS)