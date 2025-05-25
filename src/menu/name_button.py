import pygame

class Name_Button():
    def __init__(self, center_pos = (0, 0)):
        self.center = center_pos
        self.name_button_size = (350, 130)
        self.name_button_surf = pygame.surface.Surface(self.name_button_size)
        self.name_button_surf.fill((0, 0, 0))
        self.name_button_rect = self.name_button_surf.get_rect()
        self.name_button_rect.center = self.center

        self.clicked = False
        self.active = False
        self.last_submitted_name = None
        self.new_name_available = False
        self.text = ""
        self.font_size = 50
        self.font_color = pygame.Color('Green')
        self.font = pygame.font.Font(r'src\menu\font\static\PixelifySans-Bold.ttf', self.font_size)
        self.font_surf = self.font.render("Name", True, self.font_color)
        self.font_rect = self.font_surf.get_rect()
        self.font_rect.center = self.name_button_rect.center

        #
        # Cursor Settings
        self.cursor_visible = True
        self.cursor_counter = 0
        self.cursor_switch_ms = 500  

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.name_button_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.last_submitted_name = self.text
                self.new_name_available = True
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 20:
                    self.text += event.unicode

            display_text = self.text or "Name"
            if self.active and self.cursor_visible:
                display_text += "|"
            self.font_surf = self.font.render(display_text, True, self.font_color)

            self.font_rect = self.font_surf.get_rect(center=self.name_button_rect.center)

    def get_last_submitted_name(self):
        if self.new_name_available:
            self.new_name_available = False
            return self.last_submitted_name
        return None

    def render(self, screen):
        bg_color = (200, 200, 255) if self.active else (0, 0, 0)
        self.name_button_surf.fill(bg_color)

        pos_x = (screen.get_width() - self.name_button_size[0]) // 2
        pos_y = self.center[1]
        self.name_button_rect.topleft = (pos_x, pos_y)
        self.font_rect.center = self.name_button_rect.center

        screen.blit(self.name_button_surf, self.name_button_rect)
        screen.blit(self.font_surf, self.font_rect)

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.cursor_counter >= self.cursor_switch_ms:
                self.cursor_visible = not self.cursor_visible
                self.cursor_counter = current_time

        display_text = self.text
        if self.active and not self.text:
            display_text = ""

        if self.active and self.cursor_visible:
            display_text += "|"

        if not self.active and not self.text:
            display_text = "Name"

        self.font_surf = self.font.render(display_text, True, self.font_color)
        self.font_rect = self.font_surf.get_rect(center=self.name_button_rect.center)