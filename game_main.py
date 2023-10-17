import sys
import pygame
from setting import Settings
from pygame.sprite import Group
from interface import Gamestatus
from button import Button
from item_system import Weapon
from character import Character
from enemy import Enemy
from game_play import Game_play
from time import sleep
class Game():
    def __init__(self) -> None:
        pygame.init()
        self.clock=pygame.time.Clock()
        self.ai_settings=Settings()
        self.screen=pygame.display.set_mode((self.ai_settings.screen_width,self.ai_settings.screen_height))
        self.status=Gamestatus(self.screen,self.ai_settings)
        self.reset()
    def reset(self):        
        self.status.reset_stats()
        self.gp = Game_play(self.screen,self.status)
        self.left_time=self.ai_settings.max_time
    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.status.game_start and not self.status.pause:
                if event.type != pygame.KEYDOWN or event.key != pygame.K_ESCAPE: self.gp.check_event(event)
                else: self.status.check_event(event)
            else: self.status.check_event(event)

    def draw(self):
        self.screen.fill(self.ai_settings.bg_color)
        self.status.draw_page()
        self.status.show_other()
        self.status.show_game_statement()
        flag=0
        if self.status.game_over==1:flag=1
        if self.status.game_start and not self.status.pause:
            self.gp.draw()
        pygame.display.flip()    
        if flag:
            sleep(1)
            self.reset()
    def qi_dong(self):
        self.gp.play()
        if self.gp.check_score(): # 分数达标
            self.status.game_lose=0
            self.status.game_over=1
            return
        if not self.gp.check_hp(self.gp.chara) or self.left_time<=0:
            self.status.game_lose=1
            self.status.game_over=1
            return
        pass
    def run_game(self):
        while True:
            self.check_event()
            if self.status.game_start==1 and self.status.pause==0:
                self.qi_dong()
                self.left_time-=1.0/self.ai_settings.game_fps
                self.status.time=int(self.left_time)
            self.draw()
            self.clock.tick(self.ai_settings.game_fps)

game=Game()
if __name__=='__main__':
    game.run_game()