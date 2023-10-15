import pygame, sys, time, math
from item_system import Weapon
from item_system import Bullet

class Character():
    def __init__(self, setting, screen, img, weapon) -> None:
        # chara image
        self.img = img
        self.rect = self.img.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = self.rect.width, self.rect.height
        self.rect.center = self.screen_rect.center
        # chara move
        self.left, self.right, self.up, self.down = False, False, False, False
        # chara data
        self.hp = 100
        self.shield = 50
        self.speed = 10 # tbd
        self.atk_speed = 50 # tbd
        self.dmg_bonus = 0 # 伤害加成
        self.miss = 0 # 闪避率
        self.crit_rate = 0.05 #暴击暴伤
        self.crit_dmg = 0.5
        # weapon
        self.weapon = weapon
        # exp & level
        self.exp_bonus = 0
        self.level = 0
        pass

    def new_character(self, screen):
        self.rect.center = self.screen_rect.center
        self.left, self.right, self.up, self.down = False, False, False, False
        self.hp = 100
        self.shield = 50
        self.speed = 10 # tbd
        self.atk_speed = 50 # tbd
        self.dmg_bonus = 0 
        self.miss = 0 
        self.crit_rate = 0.05 
        self.crit_dmg = 0.5
        self.weapon = Weapon()
        self.exp_bonus = 0
        self.level = 0
    
    def move(self):
        #print(self.left, self.right, self.up, self.down)
        if self.left: self.rect.centerx = max(self.width / 2, self.rect.centerx - self.speed)
        if self.right: self.rect.centerx = min(self.screen_rect.width - self.width / 2, self.rect.centerx + self.speed)
        if self.up: self.rect.centery = max(self.height / 2, self.rect.centery - self.speed)
        if self.down: self.rect.centery = min(self.screen_rect.height - self.height / 2, self.rect.centery + self.speed)
        self.weapon.move()
    
    def direction(self, key, tag): # tag == 1 -> keydown or 0 --> keyup
        if tag:
            if key == pygame.K_a: self.left = True
            if key == pygame.K_d: self.right = True
            if key == pygame.K_w: self.up = True
            if key == pygame.K_s: self.down = True 
        else:
            if key == pygame.K_a: self.left = False
            if key == pygame.K_d: self.right = False
            if key == pygame.K_w: self.up = False
            if key == pygame.K_s: self.down = False

    def attack(self, mouse_x, mouse_y):
        now = time.time()
        if now - self.weapon.atk_lst < self.weapon.cd: return
        self.weapon.atk_lst = now
        print(self.rect.centerx, self.rect.centery, mouse_x, mouse_y)
        if self.weapon.type == 1:
            dirx = mouse_x - self.rect.centerx
            diry = mouse_y - self.rect.centery
            tan = math.sqrt(dirx ** 2 + diry ** 2)
            dirx /= tan 
            diry /= tan
            # rotate img
            img = pygame.image.load('weapon/knife.png')
            angle = math.degrees(math.atan(diry / dirx))
            if dirx < 0 and diry < 0:
                angle -= 180
            if dirx < 0 and diry > 0:
                angle += 180
            angle *= -1
            print(angle, diry / dirx)
            img = pygame.transform.rotate(img, angle)
            self.weapon.bullets.append(Bullet(self.rect.centerx, self.rect.centery, self.weapon.dmg, self.weapon.speed, dirx, diry, img, self.screen))
    
    def draw(self):
        self.screen.blit(self.img, self.rect)
        self.weapon.draw()
