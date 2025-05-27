from .singleton import Singleton
from .vector2 import Vector2
import pygame

class Renderer(Singleton):
    def __init__(self, camera_pos: Vector2, unit_scale: float, screen):
        super().__init__()
        
        self.camera_pos = camera_pos
        self.unit_scale = unit_scale
        self.screen = screen

        screen_width, screen_height = screen.get_size()
        scale_x = screen_width / 29
        scale_y = screen_height / 18

        self.unit_scale = min(scale_x, scale_y)

    def pixels_to_units(self, pixel_pos: Vector2):
        screen_size = Vector2.FromTuple(self.screen.get_size())
        screen_center = screen_size / 2
        delta = Vector2(
            (pixel_pos.x - screen_center.x) / self.unit_scale,
            (screen_center.y - pixel_pos.y) / self.unit_scale
        )
        return self.camera_pos + delta

    def units_to_pixels(self, pos: Vector2):
        screen_size = Vector2.FromTuple(self.screen.get_size())
        screen_center = screen_size / 2
        delta = pos - self.camera_pos
        return Vector2(
            screen_center.x + delta.x * self.unit_scale,
            screen_center.y - delta.y * self.unit_scale
        )

    def Render(self, unit_pos: Vector2, unit_size: Vector2, color=(0, 200, 0), texture: pygame.Surface = None):
        unit_pos -= Vector2(14.5, 9.0) # Center on the screen
        pixel_pos = self.units_to_pixels(unit_pos)
        pixel_size = unit_size * self.unit_scale
        rect = pygame.Rect(pixel_pos.x, pixel_pos.y - pixel_size.y, pixel_size.x, pixel_size.y)
        
        if texture:
            texture = pygame.transform.scale(texture, (int(pixel_size.x), int(pixel_size.y)))
            self.screen.blit(texture, rect)
        else:
            pygame.draw.rect(self.screen, color, rect)
