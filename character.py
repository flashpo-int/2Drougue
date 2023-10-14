import pygame, sys, time, math
from item_system import Weapon
from item_system import Bullet

class Character():
    def __init__(self, setting, screen, width, height) -> None:
        # chara image
        self.img = pygame.image.load('images\chara.png')
        self.img = pygame.transform.smoothscale(self.img, (width, height))
        self.rect = self.img.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = width, height
        # chara move
        self.left, self.right, self.up, self.down = False, False, False, False
        # chara data
        self.hp = 100
        self.shield = 50
        self.speed = 50 # tbd
        self.atk_speed = 50 # tbd
        self.dmg_bonus = 0 # 伤害加成
        self.miss = 0 # 闪避率
        self.crit_rate = 0.05 #暴击暴伤
        self.crit_dmg = 0.5
        # weapon
        self.weapon = Weapon()
        # exp & level
        self.exp_bonus = 0
        self.level = 0
        pass

    def new_character(self, screen):
        self.rect.center = self.screen_rect.center
        self.left, self.right, self.up, self.down = False, False, False, False
        self.hp = 100
        self.shield = 50
        self.speed = 50 # tbd
        self.atk_speed = 50 # tbd
        self.dmg_bonus = 0 
        self.miss = 0 
        self.crit_rate = 0.05 
        self.crit_dmg = 0.5
        self.weapon = Weapon()
        self.exp_bonus = 0
        self.level = 0
    
    def move(self):
        if self.left: self.rect.centerx = max(self.width / 2, self.rect.centerx - self.speed)
        if self.right: self.rect.centerx = max(self.screen_rect.width - self.width / 2, self.rect.centerx + self.speed)
        if self.up: self.rect.centery = max(self.height / 2, self.rect.centery - self.speed)
        if self.down: self.rect.centery = max(self.screen_rect.height - self.height / 2, self.rect.centery + self.speed)
        self.weapon.move()
    
    def direction(self, key, tag): # tag == 1 -> keydown or 0 --> keyup
        if tag:
            if key == pygame.K_LEFT: self.left = True
            if key == pygame.K_RIGHT: self.right = True
            if key == pygame.K_UP: self.up = True
            if key == pygame.K_DOWN: self.down = True 
        else:
            if key == pygame.K_LEFT: self.left = False
            if key == pygame.K_RIGHT: self.right = False
            if key == pygame.K_UP: self.up = False
            if key == pygame.K_DOWN: self.down = False

    def attack(self, mouse_x, mouse_y):
        now = time.time()
        if now - self.weapon.atk_lst < self.weapon.cd: return
        self.weapon.atk_lst = now
        if self.type == 1:
            dirx = mouse_x - self.rect.centerx
            diry = mouse_y - self.rect.centery
            tan = math.sqrt(dirx ** 2 + diry ** 2)
            dirx /= tan 
            diry /= tan
            self.weapon.bullets.append(Bullet(self.rect.centerx, self.rect.centery, self.weapon.dmg, self.weapon.speed, dirx, diry, self.weapon.img, self.screen))
    
    def draw(self):
        self.screen.blit(self.img, self.rect)
        self.weapon.draw()
