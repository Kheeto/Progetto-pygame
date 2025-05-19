import pygame
import sys

pygame.init()

UNIT_SCALE = 10
CAMERA_SPEED = 1
ZOOM_SPEED = 1.1

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Gioco fighissimo")
clock = pygame.time.Clock()

camera_pos = [0.0, 0.0]
unit_scale = UNIT_SCALE

obj_unit_pos = (10, 10)
obj_unit_size = (2, 2)

def units_to_pixels(pos, screen_size):
    screen_center = (screen_size[0] / 2, screen_size[1] / 2)
    delta = (pos[0] - camera_pos[0], pos[1] - camera_pos[1])
    return (
        screen_center[0] + delta[0] * unit_scale,
        screen_center[1] - delta[1] * unit_scale
    )

def units_to_pixels_size(size):
    return size[0] * unit_scale, size[1] * unit_scale

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Zoom
        elif event.type == pygame.MOUSEWHEEL:
            screen_size = screen.get_size()
            screen_center = (screen_size[0] / 2, screen_size[1] / 2)

            world_x = camera_pos[0]
            world_y = camera_pos[1]

            old_scale = unit_scale
            if event.y > 0:
                unit_scale *= ZOOM_SPEED
            elif event.y < 0:
                unit_scale /= ZOOM_SPEED

            scale_ratio = old_scale / unit_scale

            camera_pos[0] = world_x + (screen_center[0] - screen_center[0]) / unit_scale * (1 - scale_ratio)
            camera_pos[1] = world_y - (screen_center[1] - screen_center[1]) / unit_scale * (1 - scale_ratio)

    # Input
    keys = pygame.key.get_pressed()
    delta = CAMERA_SPEED / unit_scale
    if keys[pygame.K_LEFT]:
        camera_pos[0] -= delta
    if keys[pygame.K_RIGHT]:
        camera_pos[0] += delta
    if keys[pygame.K_UP]:
        camera_pos[1] += delta
    if keys[pygame.K_DOWN]:
        camera_pos[1] -= delta

    screen_size = screen.get_size()
    screen.fill((30, 30, 30))

    # Rendering
    pixel_pos = units_to_pixels(obj_unit_pos, screen_size)
    pixel_size = units_to_pixels_size(obj_unit_size)
    rect = pygame.Rect(pixel_pos[0], pixel_pos[1] - pixel_size[1], pixel_size[0], pixel_size[1])
    pygame.draw.rect(screen, (0, 200, 0), rect)

    pygame.display.flip()
    clock.tick(60)