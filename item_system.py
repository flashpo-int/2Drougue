import pygame, sys, time

class Bullet():
    def __init__(self, x, y, dmg, speed, dirx, diry, img, screen) -> None:
        self.dmg, self.speed, self.dirx, self.diry = dmg, speed, dirx, diry
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.screen = screen
        pass
    
    def check(self, screen_rect): # 检查是否离开屏幕
        if self.rect.centerx > screen_rect.width or self.rect.centerx < 0 or self.rect.centery > screen_rect.height or self.rect.centery < 0:
            return False
        return True
    
    def draw(self):
        self.screen.blit(self.img, self.rect)


class Weapon():
    def __init__(self, name, dmg, type, cd, speed, img, screen) -> None: # 名称 伤害 近战0/远程1 冷却
        self.name, self.dmg, self.type, self.cd, self.speed, self.img = name, dmg, type, cd, speed, img
        self.screen_rect = screen.get_rect()
        self.bullets = []
        self.atk_lst = -self.cd # 处理攻击间隔
        pass

    def move(self):
        if not self.type: return
        for bullet in self.bullets:
            bullet.rect.centerx += bullet.speed * bullet.dirx
            bullet.rect.centery += bullet.speed * bullet.diry

    def draw(self):
        for bullet in self.bullets:
            if bullet.check(self.screen_rect) == False:
                self.bullets.remove(bullet)
            bullet.draw()