import pygame
from characters import *
from characters.projectile import Projectile
from core import *
from ai import *

class Dwarf(Character):
    def __init__(self, id: int = -1, tags: list[str] = [], position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1),
                 rotation: float = 0.0, color = (255, 255, 255), agent: Agent = None, targetTags : list[str] = [], flip = False):
        super().__init__(id, tags, position, scale, rotation, color, agent, 0.0, targetTags)

        self.animations = {
            'idle': self.load_animation('cannon_', 1),
            'blink': self.load_animation('cannon_blink_', 1),
            'shoot': self.load_animation('cannon_shoot_', 2)
        }
        self.current_action = 'idle'
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 100
        self.timer = 0.0
        self.attack_timer = 0.0
        self.attack_delay = 3
        self.blink_timer = 0.0
        self.blink_delay = 3.5
        self.attack_distance = 9
        self.flip = flip

    def load_animation(self, base_name, count):
        return [ pygame.image.load(f'src/img/{base_name}{i}.png').convert_alpha() for i in range(1, count + 1) ]

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
                if self.current_action in ['shoot', 'blink']:
                    self.current_action = 'idle'
                    self.current_frame = 0
                else:
                    self.current_frame = 0  # animazioni cicliche
    
    def Update(self, dt: float):
        self.agent.UpdatePosition(self.position)

        self.direction = self.agent.GetDirection()
        
        if self.direction is not None:
          if Vector2.Distance(self.position, self.agent.target) < self.attack_distance:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_delay:
                self.attack_timer = 0
                self.play('shoot')
                self.Shoot(self.agent.target - self.position)
            self.blink_timer += dt
            if self.current_action == 'idle' and self.blink_timer >= self.blink_delay:
                self.blink_timer = 0
                self.play('blink')
          else:
            self.blink_timer += dt
            if self.current_action == 'idle' and self.blink_timer >= self.blink_delay:
                self.blink_timer = 0
                self.play('blink')

        self.LookForTargets()
        self.update_animation(dt)

        self.health.position = self.position + Vector2(0.5, 1.5)
        if self.health.current_life <= 0:
           # Dead
           GameObjectManager.instance.delQueue.append(self)

    def Render(self):
        self.texture = pygame.transform.flip(self.animations[self.current_action][self.current_frame], self.flip, False)
        super().Render()
    
    # Shoot cannonball
    def Shoot(self, direction):
        direction = direction.Normalized()

        projectile = Projectile(
            id=-1, tags=["projectile"], position=self.position + Vector2(-0.5 if self.flip else 1.5,0.4 if self.flip else 0.5), scale=Vector2(1, 1),
            rotation=0, color=(255,255,255), texture=pygame.image.load("src/img/cannonball.png").convert_alpha(), direction=direction, speed=15,
            damage=35
        )
        GameObjectManager.instance.addQueue.append(projectile)
