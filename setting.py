import pygame
pygame.init()
class Settings():
    def __init__(self):
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        self.small_screen_width= self.screen_width // 1.2
        self.small_screen_height= self.screen_height // 1.2
        self.bg_color = (230, 230, 230)
        self.small_bg_color=(100,100,100)