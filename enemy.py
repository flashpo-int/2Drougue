import pygame, sys, random, math, time

class Enemy():
    def __init__(self, hp, dmg, speed, cd, img, screen, weapon) -> None:
        self.hp, self.dmg, self.speed, self.cd, self.img = hp, dmg, speed, cd, img
        # last atk
        self.atk_lst = -cd
        # direction
        self.dirx, self.diry = 0, 0
        # rect
        self.rect = self.img.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect.centerx = random.random() * self.screen_rect.width
        self.rect.centery = random.random() * self.screen_rect.height
        # 4 direction to appear up down left right
        tag = random.randint(1, 4)
        if tag == 1:
            self.rect.centery = -self.rect.height / 2
        elif tag == 2:
            self.rect.centery = self.screen_rect.height + self.rect.height / 2
        elif tag == 3:
            self.rect.centerx = -self.rect.width / 2
        elif tag == 4:
            self.rect.centerx = self.screen_rect.width + self.rect.width / 2
        pass
        # weapon
        self.weapon = weapon
        # level
        self.level = 0

    def move(self):
        self.rect.centerx += self.dirx * self.speed
        self.rect.centery += self.diry * self.speed
        if self.weapon != None: self.weapon.move()
    
    def direction(self, chara_x, chara_y):
        dirx = chara_x - self.rect.centerx
        diry = chara_y - self.rect.centery
        tan = math.sqrt(dirx ** 2 + diry ** 2)
        if tan == 0: self.dirx = self.diry = 0
        else: self.dirx, self.diry = dirx / tan, diry / tan
    
    def draw(self):
        self.screen.blit(self.img, self.rect)

    def attack(self):
        cur = time.time()
        if cur - self.atk_lst < self.cd: return 0
        self.atk_lst = cur
        return self.dmg