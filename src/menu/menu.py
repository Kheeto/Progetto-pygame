# import pygame
# from host_button import Host_Button
# from name_button import Name_Button
# from join_button import Join_Button
# from ip_button import Ip_Button
# from sys import exit

# # Functiont that Creates Blurred Image
# def blur_surface(surface, amount=8):
#     scale = (surface.get_width() // amount, surface.get_height() // amount)
#     small = pygame.transform.smoothscale(surface, scale)
#     blurred = pygame.transform.smoothscale(small, surface.get_size())
#     return blurred

# # Functiont that Allows to Risize Background
# def scale_background_to_screen(background_surf, screen_size):
#     bg_width, bg_height = background_surf.get_size()
#     screen_width, screen_height = screen_size

#     scale_w = screen_width / bg_width
#     scale_h = screen_height / bg_height

#     scale = max(scale_w, scale_h)

#     new_width = int(bg_width * scale)
#     new_height = int(bg_height * scale)

#     scaled_bg = pygame.transform.smoothscale(background_surf, (new_width, new_height))

#     rect = scaled_bg.get_rect(center=(screen_width//2, screen_height//2))
#     return scaled_bg, rect

# pygame.init()

# FPS = 60

# screen = pygame.display.set_mode((1188, 737), pygame.RESIZABLE)
# pygame.display.set_caption("Gioco fighissimo")
# clock = pygame.time.Clock()
# screen_size = screen.get_size()

# menu_background_surf = pygame.image.load(r'src\img\Background.png').convert()
# menu_blur_background_surf = blur_surface(menu_background_surf, amount=20)

# # Buttons
# name_button_obj = Name_Button()
# name_button_obj.center = (None, 43)

# host_button_obj = Host_Button()
# host_button_obj.center = (None, 216)

# ip_button_obj = Ip_Button()
# ip_button_obj.center = (None, 389)

# join_button_obj = Join_Button()
# join_button_obj.center = (None, 562)

# while True:
#     screen_size = screen.get_size()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()

#         # Keyboard Events Handling
#         name_button_obj.handle_event(event)
#         ip_button_obj.handle_event(event)    

#     # Getting the Name of the Player
#     new_name = name_button_obj.get_last_submitted_name()
    
#     if new_name:
#         player_name = new_name
#         print('Name:',player_name)

#     # Getting the Ip of the Player
#     new_ip = ip_button_obj.get_last_submitted_ip()
    
#     if new_ip:
#         player_ip = new_ip
#         print('Ip:', new_ip)

#     #
#     name_button_obj.update()
#     ip_button_obj.update()

#     # Resizing ONLY Background when Changing Screen size
#     menu_blur_background_surf, rect = scale_background_to_screen(menu_blur_background_surf, screen.get_size())
#     screen.blit(menu_blur_background_surf, rect)
    
#     # Rendering the Buttons
#     name_button_obj.render(screen)
#     host_button_obj.render(screen)
#     ip_button_obj.render(screen)
#     join_button_obj.render(screen)

#     pygame.display.flip()
#     clock.tick(FPS)

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