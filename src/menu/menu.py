import pygame
from menu.host_button import Host_Button
from menu.name_button import Name_Button
from menu.join_button import Join_Button
from menu.ip_button import Ip_Button

def blur_surface(surface, amount=8):
    scale = (surface.get_width() // amount, surface.get_height() // amount)
    small = pygame.transform.smoothscale(surface, scale)
    blurred = pygame.transform.smoothscale(small, surface.get_size())
    return blurred

def scale_background_to_screen(background_surf, screen_size):
    bg_width, bg_height = background_surf.get_size()
    screen_width, screen_height = screen_size

    scale_w = screen_width / bg_width
    scale_h = screen_height / bg_height
    scale = max(scale_w, scale_h)

    new_width = int(bg_width * scale)
    new_height = int(bg_height * scale)

    scaled_bg = pygame.transform.smoothscale(background_surf, (new_width, new_height))
    rect = scaled_bg.get_rect(center=(screen_width // 2, screen_height // 2))
    return scaled_bg, rect

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_background_surf = pygame.image.load(r'src\img\Background.png').convert()
        self.menu_blur_background_surf = blur_surface(self.menu_background_surf, amount=20)

        self.name_button = Name_Button()
        self.name_button.center = (None, 43)

        self.host_button = Host_Button()
        self.host_button.center = (None, 216)

        self.ip_button = Ip_Button()
        self.ip_button.center = (None, 389)

        self.join_button = Join_Button()
        self.join_button.center = (None, 562)

        self.player_name = None
        self.player_ip = None

        self.next_screen = None

    def handle_event(self, event):
        self.name_button.handle_event(event)
        self.ip_button.handle_event(event)

    def update(self):
        new_name = self.name_button.get_last_submitted_name()
        if new_name:
            self.player_name = new_name
            print('Name:', self.player_name)

        new_ip = self.ip_button.get_last_submitted_ip()
        if new_ip:
            self.player_ip = new_ip
            print('Ip:', self.player_ip)

        self.name_button.update()
        self.ip_button.update()
        self.host_button.update()
        self.join_button.update()

        if self.host_button.clicked:
            self.next_screen = "host"
        elif self.join_button.clicked:
            self.next_screen = "join"

    def render(self):
        screen_size = self.screen.get_size()
        self.menu_blur_background_surf, rect = scale_background_to_screen(
            self.menu_blur_background_surf, screen_size
        )
        self.screen.blit(self.menu_blur_background_surf, rect)

        self.name_button.render(self.screen)
        self.host_button.render(self.screen)
        self.ip_button.render(self.screen)
        self.join_button.render(self.screen)