import pygame, sys, time, math, random
from item_system import Weapon
from item_system import Bullet

exp = lambda x: x**2 + 6 * x + 9 # 每级所需经验
gain = lambda x, tag: 0.05 * x ** 2 + 0.30 * x + 9 if not tag else 0 # 击杀每只小/大怪可获得经验 ## + 0.45

class Character():
    def __init__(self, setting, screen, status, img, weapon) -> None:
        # chara image
        self.img = img
        self.status=status
        self.rect = self.img.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = self.rect.width, self.rect.height
        self.rect.center = self.screen_rect.center
        # chara move
        self.left, self.right, self.up, self.down = False, False, False, False
        # chara data
        self.hp = 100
        self.hp_max = 100 # 最大生命
        self.hp_bonus = 1 # 生命加成
        self.shield = 50
        self.shield_max = 50 # 最大护甲值
        self.shield_bonus = 1 # 护甲加成 (##可能除0直接炸了##后面加了if)
        self.shield_cd = 3 # 护甲回复cd
        self.shield_lst = -3 # 记录上一次回复
        self.speed = 10 # tbd
        self.atk_speed = 50 # tbd
        self.dmg_bonus = 1 # 伤害加成
        self.miss = 0 # 闪避率
        self.crit_rate = 0.05 # 暴击
        self.crit_dmg = 0.5 #暴伤
        self.distant_dmg = 0 # 远程伤害（角色本身）
        self.near_dmg = 0 # 近战伤害（角色本身）
        # weapon
        self.weapon = weapon
        # exp & level
        self.exp_bonus = 0
        self.level = 0 # 最高16级
        self.exp_need = exp(0)
        # skill1 --  潜能爆发
        self.buff1 = False
        self.cd1 = 10
        self.lst1 = -self.cd1
        self.time1 = 10
        # skill2 -- 铁甲护佑
        self.buff2 = False
        self.cd2 = 10
        self.lst2 = -self.cd2
        self.time2 = 3
        # skill3 -- 幻影突袭
        self.buff3 = False
        self.cd3 = 10
        self.lst3 = -self.cd3
        self.time3 = 3
        pass
    
    def move(self):
        if self.status.bao==1:
            self.status.bao=0
            self.left=self.right=self.up=self.down=0
        #print(self.left, self.right, self.up, self.down)
        if self.left: self.rect.centerx = max(self.width / 2, self.rect.centerx - self.speed)
        if self.right: self.rect.centerx = min(self.screen_rect.width - self.width / 2, self.rect.centerx + self.speed)
        if self.up: self.rect.centery = max(self.height / 2, self.rect.centery - self.speed)
        if self.down: self.rect.centery = min(self.screen_rect.height - self.height / 2, self.rect.centery + self.speed)
        self.weapon.move()
    
    def direction(self, key, tag): # tag == 1 -> keydown or 0 --> keyup

        if key == pygame.K_a or key==pygame.K_LEFT: self.left = tag
        if key == pygame.K_d or key==pygame.K_RIGHT: self.right = tag
        if key == pygame.K_w or key==pygame.K_UP: self.up = tag
        if key == pygame.K_s or key==pygame.K_DOWN: self.down = tag


            
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
            img = self.weapon.img
            angle = math.degrees(math.atan(diry / dirx))
            if dirx < 0 and diry < 0:
                angle -= 180
            if dirx < 0 and diry > 0:
                angle += 180
            angle *= -1
            img = pygame.transform.rotate(img, angle)
            self.weapon.bullets.append(Bullet(self.rect.centerx, self.rect.centery, self.weapon.dmg, self.weapon.speed, dirx, diry, img, self.screen))
    
    def draw(self):
        self.screen.blit(self.img, self.rect)
        self.weapon.draw()
        if self.buff2: # 贴盾的图
            pass

    def get_exp(self, tag):
        if self.level == 16: return
        exps = gain(self.level, tag)
        extra = max(exps - self.exp_need, 0)
        self.exp_need -= exps
        if self.exp_need <= 0:
            self.level += 1
            self.exp_need = exp(self.level)
            self.exp_need -= extra

    def hp_up(self, delta):
        self.hp *= (self.hp_bonus + delta) / self.hp_bonus
        self.hp_max *= (self.hp_bonus + delta) / self.hp_bonus
        self.hp_bonus += delta

    def shield_up(self, delta):
        self.shield *= (self.shield_bonus + delta) / self.shield_bonus
        self.shield_max *= (self.shield_bonus + delta) / self.shield_bonus
        self.shield_bonus += delta

    def get_buff(self, type, level): # 获得buff， type表示类别，level稀有度
        if type == 1: # 最大生命值加成
            if level == 1: self.hp_up(0.1)
            elif level == 2: self.hp_up(0.2)
            elif level == 3: self.hp_up(0.25)
        elif type == 2: # 护甲加成
            if level == 1: self.shield_up(0.1)
            elif level == 2: self.shield_up(0.2)
            elif level == 3: self.shield_up(0.25)
        elif type == 3: # 伤害加成
            if level == 1: self.dmg_bonus += 0.05
            elif level == 2: self.dmg_bonus += 0.08
            elif level == 3: self.dmg_bonus += 0.10
        elif type == 4: # 暴击率
            if level == 1: self.crit_rate += 0.03
            elif level == 2: self.crit_rate += 0.06
            elif level == 3: self.crit_rate += 0.09
        elif type == 5: # 暴击伤害
            if level == 1: self.crit_dmg += 0.10
            elif level == 2: self.crit_dmg += 0.15
            elif level == 3: self.crit_dmg += 0.20
        elif type == 6: # 闪避率
            if level == 1: self.miss += 0.03
            elif level == 2: self.miss += 0.05
            elif level == 3: self.miss += 0.08
        self.hp=self.hp_max
    def judge_crit(self):
        flag = random.random()
        return True if flag <= self.crit_rate else False

    def get_damage(self):
        if self.weapon.type: # 武器是远程
            basis = (self.weapon.dmg + self.distant_dmg) * self.dmg_bonus
            return basis * (1 + self.crit_dmg) if self.judge_crit() else basis # 暴击与否
        else:
            basis = (self.weapon.dmg + self.near_dmg) * self.dmg_bonus
            return basis * (1 + self.crit_dmg) if self.judge_crit() else basis # 暴击与否
        
    def get_hurt(self, dmg):
        if self.buff2: return # buff2 is on, won't get hurt
        extra = dmg - self.shield
        self.shield = max(0, self.shield - dmg)
        if extra <= 0: return
        self.hp -= extra

    def get_shield(self):
        cur = time.time()
        if cur - self.shield_lst < self.shield_cd or self.shield == self.shield_max: return
        #print(self.shield_lst, cur, self.shield)
        self.shield_lst = cur
        self.shield = min(self.shield_max, self.shield + 1)
        
    def get_skill(self, key):
        if key == pygame.K_q: # q skill
            cur = time.time()
            if cur - self.lst1 < self.cd1 or self.buff1: return
            self.lst1 = cur
            self.buff1 = True
            self.weapon.cd /= 2
            self.rect.width *= 1.25
            self.rect.height *= 1.25
            self.img = pygame.transform.smoothscale(self.img, (self.rect.width, self.rect.height))
        elif key == pygame.K_f: # f skill
            cur = time.time()
            if cur - self.lst2 < self.cd2 or self.buff2: return
            self.lst2 = cur
            self.buff2 = True
        elif key == pygame.K_e: # e skill
            cur = time.time()
            if cur - self.lst3 < self.cd3 or self.buff3: return
            self.lst3 = cur
            self.buff3 = True
            self.speed *= 2
    
    def check_skill(self):
        cur = time.time()
        if self.buff1 and cur - self.lst1 >= self.time1:
            self.buff1 = False
            self.lst1 = cur
            self.weapon.cd *= 2
            self.rect.width /= 1.25
            self.rect.height /= 1.25
            self.img = pygame.transform.smoothscale(self.img, (self.rect.width, self.rect.height))

        if self.buff2 and cur - self.lst2 >= self.time2:
            self.buff2 = False
            self.lst2 = cur
        if self.buff3 and cur - self.lst3 >= self.time3:
            self.buff3 = False
            self.lst3 = cur
            self.speed /= 2