import sys
import pygame
from setting import Settings
from pygame.sprite import Group
from interface import Gamestatus
from button import Button
import time
class Game():
    def __init__(self) -> None:
        pygame.init()
        self.clock=pygame.time.Clock()
        self.ai_settings=Settings()
        self.screen=pygame.display.set_mode((self.ai_settings.screen_width,self.ai_settings.screen_height))
        self.reset()
    def reset(self):        
        # self.status.game_over=FLAG
        self.status=Gamestatus(self.screen,self.ai_settings)
        # self.status.easy=0
    def check_event(self):
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y=pygame.mouse.get_pos()
                self.status.turn_page(mouse_x,mouse_y)
    def draw(self):
        self.screen.fill(self.ai_settings.bg_color)
        self.status.draw_page()
        pygame.display.flip()    
    def run_game(self):
        while True:
            self.check_event()
            self.draw()
            self.clock.tick(60)

game=Game()
if __name__=='__main__':
    game.run_game()