'''
game_rules.py:定义游戏的规则，包括得分、目标、任务、胜利条件和失败条件。



单局游戏时长记为 15min

每5min出一个boss

以活下来（倒计时结束）/击杀三个boss
或者血量清0        作为单局结束条件

根据击杀的小怪和boss数目来统计纯粹能量（局外提升）的获取
纯粹能量= 击杀的小怪数*log10（i）+i +boss数*30，i为击杀小怪数
'''

import pygame, sys, time, random
from character import Character
from item_system import Weapon
from enemy import Enemy
from interface import Gamestatus
from setting import *
class Game_play():
    def __init__(self, screen,status) -> None:
        self.chara = None
        self.status=status
        self.enemy = []
        self.screen = screen
        # data_class
        # weapon
        self.arrow = Weapon("arrow", 10, 1, 1.5, 5, arrow, self.screen)
        self.knife = Weapon("knife", 5, 1, 1.01, 10, knife, self.screen)
        # character
        self.chara_1 = Character(Settings, self.screen,self.status, chara1, self.knife)
        # enemy
        self.enemy_1 = Enemy(10, 10, 2.5, 1, enemy1, self.screen, None)
        # setting:
        self.enemy_cd = 5
        self.enemy_lst = -5

        # score:
        self.score = 0

        self.create_chara()
        pass

    def create_chara(self):
        self.chara = self.chara_1

    def create_enemy(self):
        cur = time.time()
        if cur - self.enemy_lst < self.enemy_cd: return
        self.enemy_lst = cur 
        choose = random.randint(0, 1)
        # test enemy --> enemy1
        new_one = Enemy(10, 10, 5, 1, enemy1, self.screen, None)
        self.enemy.append(new_one)
    
    def direction_chara(self, key, tag): # tag == 1 -> keydown or 0 --> keyup
        self.chara.direction(key, tag)
    
    def move(self):
        self.chara.move()
        for enemy in self.enemy:
            enemy.direction(self.chara.rect.centerx, self.chara.rect.centery)
            enemy.move()
    
    def check_colli(self, a, b):
        return pygame.sprite.collide_rect(a, b)
    
    def check_hp(self, a):
        if a.hp <=0: return False
        return True
    
    def chara_attack(self):
        for bullet in self.chara.weapon.bullets:
            for enemy in self.enemy:
                if self.check_colli(bullet, enemy):
                    enemy.hp -= self.chara.get_damage() # 敌人受到攻击扣血
                    if bullet in self.chara.weapon.bullets:
                        self.chara.weapon.bullets.remove(bullet)
                    if not self.check_hp(enemy): # 击杀小怪
                        self.enemy.remove(enemy)
                        self.score += 5
                        self.chara.get_exp(0)

    def enemy_attack(self):
        for enemy in self.enemy:
            if self.check_colli(enemy, self.chara):
                self.chara.get_hurt(enemy.attack())

    def draw(self):
        self.chara.draw()
        for enemy in self.enemy:
            enemy.draw()
        pygame.display.flip()

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.direction_chara(event.key, 1)
        elif event.type == pygame.KEYUP:
            self.direction_chara(event.key, 0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.chara.attack(mouse_x, mouse_y)

    def check_score(self):
        if self.score >= max_score: return True
        return False

    def play(self):
        self.create_enemy()
        self.move()
        self.chara_attack()
        self.enemy_attack()
        self.chara.get_shield()
        self.status.chara=self.chara
        self.status.enemy=self.enemy
        self.status.score=self.score
        print(self.chara.hp, self.chara.shield)
        