import pygame

class Host_Button():
    def __init__(self, center_pos = (0,0)):    
        self.center = center_pos
        
        # General Surface Settings
        self.host_button_size = (300,130)
        self.host_button_surf = pygame.surface.Surface(self.host_button_size)
        self.host_button_surf.fill((255,255,255))

        self.host_button_rect = self.host_button_surf.get_rect()
        self.host_button_rect.center = self.center

        self.clicked = False
        self.was_pressed = False

        # Text Surface Settings
        self.font_size = 50
        self.font_color = 'Green'
        self.font = pygame.font.Font(r'src\menu\font\static\PixelifySans-Bold.ttf', self.font_size)
        self.font_surf = self.font.render("Host", True, self.font_color)
        self.font_rect = self.font_surf.get_rect()
        self.font_rect.center = self.host_button_rect.center

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click_sx = pygame.mouse.get_pressed()[0]

        if self.host_button_rect.collidepoint(mouse_pos):
            if mouse_click_sx and not self.was_pressed:
                self.was_pressed = True
                return True
            elif not mouse_click_sx:
                self.was_pressed = False
        else:
            self.was_pressed = False

        return False

    def render(self, screen):
        # Handling click events
        if self.is_clicked():
            if not self.clicked:
                self.host_button_surf.fill('Red')
                self.clicked = True
            else:
                self.host_button_surf.fill('White')
                self.clicked = False

        pos_x = (screen.get_width() - self.host_button_size[0]) // 2
        pos_y = self.center[1]

        self.host_button_rect.topleft = (pos_x, pos_y)
        self.font_rect.center = self.host_button_rect.center
        
        screen.blit(self.host_button_surf, self.host_button_rect)
        screen.blit(self.font_surf, self.font_rect)
