# import pygame
# from characters.character import Character

# def resize_image(image, new_width, new_height):
#     return pygame.transform.scale(image, (new_width, new_height))

# class Elf(Character):
#     def __init__(self, agent=None, speed=0):
#         super().__init__(agent, speed)
#         self.life = 100
#         self.size = (100, 100)

#         self.raw_img = pygame.image.load(r'src\img\elf\elf_1.png').convert_alpha()
#         self.img = resize_image(self.raw_img, *self.size)
#         self.rect = self.img.get_rect()
#         self.rect.center = (123, 123)

#         self.animations = {
#             'idle': self.load_animation('elf_', 3),
#             'run': self.load_animation('elf_run_', 6),
#             'blink': self.load_animation('elf_blink_', 3),
#             'shoot': self.load_animation('elf_shoot_', 9)
#         }

#         self.current_action = 'idle'
#         self.current_frame = 0
#         self.last_update = pygame.time.get_ticks()
#         self.frame_delay = 100

#     def load_animation(self, base_name, count):
#         return [
#             resize_image(
#                 pygame.image.load(f'src/img/elf/{base_name}{i}.png').convert_alpha(),
#                 *self.size
#             ) for i in range(1, count + 1)
#         ]

#     def play(self, action_name):
#         if self.current_action != action_name:
#             self.current_action = action_name
#             self.current_frame = 0
#             self.last_update = pygame.time.get_ticks()

#     def update_animation(self):
#         now = pygame.time.get_ticks()
#         if now - self.last_update > self.frame_delay:
#             self.last_update = now
#             self.current_frame += 1
#             if self.current_frame >= len(self.animations[self.current_action]):
#                 # Torna a idle dopo un'azione non ciclica (come blink o shoot)
#                 if self.current_action in ['blink', 'shoot']:
#                     self.current_action = 'idle'
#                     self.current_frame = 0
#                 else:
#                     self.current_frame = 0  # animazioni cicliche

#     def render(self, screen, pos):
#         self.update_animation()
#         current_img = self.animations[self.current_action][self.current_frame]
#         screen.blit(current_img, pos)

#     def blink(self):
#         self.play('blink')

#     def run(self):
#         self.play('run')

#     def shoot(self):
#         self.play('shoot')


import pygame
from core.vector2 import Vector2
from core.renderer import Renderer
from ai.agent import Agent
from characters.character import Character

class Elf(Character):
    def __init__(self, id: int = -1, tags: list[str] = [], position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1),
                 rotation: float = 0.0, color = (255, 255, 255), agent: Agent = None, speed = float(1), targetTags : list[str] = [], flip = False):
        super().__init__(id, tags, position, scale, rotation, color, agent, speed, targetTags)

        self.animations = {
            'idle': self.load_animation('elf_', 3),
            'run': self.load_animation('elf_run_', 6),
            'blink': self.load_animation('elf_blink_', 3),
            'shoot': self.load_animation('elf_shoot_', 9)
        }
        self.current_action = 'idle'
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 100
        self.timer = 0.0
        self.flip = flip

    def load_animation(self, base_name, count):
        return [ pygame.image.load(f'src/img/elf/{base_name}{i}.png').convert_alpha() for i in range(1, count + 1) ]

    def play(self, action_name):
        if self.current_action != action_name:
            self.current_action = action_name
            self.current_frame = 0
            self.timer = 0.0

    def update_animation(self, dt: float):
        self.timer += dt * 1800
        if self.timer > self.frame_delay:
            self.timer = 0.0
            self.current_frame += 1
            if self.current_frame >= len(self.animations[self.current_action]):
                # Torna a idle dopo un'azione non ciclica (come blink o shoot)
                if self.current_action in ['blink', 'shoot']:
                    self.current_action = 'idle'
                    self.current_frame = 0
                else:
                    self.current_frame = 0  # animazioni cicliche
    
    def Update(self, dt: float):
        super().Update(dt)

        if self.direction is not None and self.direction != Vector2(0.0, 0.0):
            self.play('run')

        self.update_animation(dt)

    def Render(self):
        self.texture = pygame.transform.flip(self.animations[self.current_action][self.current_frame], self.flip, False)
        super().Render()

    def blink(self):
        self.play('blink')

    def run(self):
        self.play('run')

    def shoot(self):
        self.play('shoot')