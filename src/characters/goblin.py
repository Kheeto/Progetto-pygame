import pygame
from characters.character import Character
from core.vector2 import Vector2
from core.gameobjectmanager import GameObjectManager
from ai.agent import Agent

class Goblin(Character):
    def __init__(self, id: int = -1, tags: list[str] = [], position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1),
                 rotation: float = 0.0, color = (255, 255, 255), agent: Agent = None, speed = float(1), targetTags : list[str] = [], flip = False):
        super().__init__(id, tags, position, scale, rotation, color, agent, speed, targetTags)

        self.animations = {
            'idle': self.load_animation('goblin_', 5),
            'run': self.load_animation('goblin_run_', 8),
            'attack': self.load_animation('goblin_attack_', 4)
        }
        self.current_action = 'idle'
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 100
        self.timer = 0.0
        self.attack_timer = 0.0
        self.attack_delay = 1.5
        self.stop_distance = 0.5
        self.flip = flip
        self.damage = 15

    def load_animation(self, base_name, count):
        return [ pygame.image.load(f'src/img/goblin/{base_name}{i}.png').convert_alpha() for i in range(1, count + 1) ]

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
                if self.current_action in ['attack']:
                    self.current_action = 'idle'
                    self.current_frame = 0
                else:
                    self.current_frame = 0  # animazioni cicliche
    
    def Update(self, dt: float):
        self.agent.UpdatePosition(self.position)

        self.direction = self.agent.GetDirection()
        if self.direction is not None:
          if Vector2.Distance(self.position, self.agent.target) < self.stop_distance:
            self.direction = Vector2(0, 0)
            if self.current_action == 'run': self.play('idle')
            self.attack_timer += dt
            if self.attack_timer >= self.attack_delay:
                self.attack_timer = 0
                self.play('attack')
                self.currentTarget.health.take_damage(self.damage)
          else:
            self.position += self.direction * self.speed * dt
            self.play('run')

        self.LookForTargets()
        self.update_animation(dt)

        self.health.position = self.position + Vector2(0.3, 1.5)
        if self.health.current_life <= 0:
           # Dead
           GameObjectManager.instance.delQueue.append(self)

    def Render(self):
        self.flip = self.direction is None or self.direction.x < 0
        self.texture = pygame.transform.flip(self.animations[self.current_action][self.current_frame], self.flip, False)
        super().Render()