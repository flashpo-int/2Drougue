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
from setting import Settings
from interface import Gamestatus

# enemy size
enemy_width = 5
enemy_height = 10

# character size
chara_width = 10
chara_height = 15

# weapon size
weapon_width = 10
weapon_height = 5

# character image
enemy1 = pygame.image.load('character\enemy1\sprite1.png')
#enemy1 = pygame.transform.smoothscale(enemy1, (enemy_width, enemy_height))
enemy2 = pygame.image.load('character\enemy2\sprite1.png')
#enemy2 = pygame.transform.smoothscale(enemy2, (enemy_width, enemy_height))
enemy3 = pygame.image.load('character\enemy3\sprite1.png')
#enemy3 = pygame.transform.smoothscale(enemy3, (enemy_width, enemy_height))
chara1 = pygame.image.load('character\character1\char1.png')
#chara1 = pygame.transform.smoothscale(chara1, (chara_width, chara_height))

# weapon image
arrow = pygame.image.load('weapon/arrow.png')
bow = pygame.image.load('weapon/bow.png')
knife = pygame.image.load('weapon/knife.png')
shield = pygame.image.load('weapon/shield.png')
sword = pygame.image.load('weapon/sword.png')

# score
max_score = 100

class Game_play():
    def __init__(self, screen) -> None:
        self.chara = None
        self.enemy = []
        self.screen = screen
        # data_class
        # weapon
        self.arrow = Weapon("arrow", 10, 1, 1.5, 5, arrow, self.screen)
        self.knife = Weapon("knife", 5, 1, 1.01, 10, knife, self.screen)
        # character
        self.chara_1 = Character(Settings, self.screen, chara1, self.knife)
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
                    enemy.hp -= bullet.dmg
                    if bullet in self.chara.weapon.bullets:
                        self.chara.weapon.bullets.remove(bullet)
                    if not self.check_hp(enemy):
                        self.enemy.remove(enemy)
                        self.score += 5

    def enemy_attack(self):
        for enemy in self.enemy:
            if self.check_colli(enemy, self.chara):
                self.chara.hp -= enemy.attack()

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

    def play(self,status):
        self.create_enemy()
        self.move()
        self.chara_attack()
        self.enemy_attack()
        status.chara=self.chara
        status.enemy=self.enemy
        