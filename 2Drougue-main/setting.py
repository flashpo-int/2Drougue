import pygame
pygame.init()

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

class Settings():
    def __init__(self):
        self.screen_info = pygame.display.Info()
        #self.screen_width = self.screen_info.current_w
        #self.screen_height = self.screen_info.current_h
        self.screen_width = 1500
        self.screen_height = 800
        self.small_screen_width= self.screen_width // 1.2
        self.small_screen_height= self.screen_height // 1.2
        self.bg_color = (230, 230, 230)
        self.small_bg_color=(100,100,100)
    def save(self,what):
        self.recod=what # 不知道写啥，快点告诉我保存什么
        #把你们要保存的写在这里

        ##天赋界面的提升情况
        ##纯粹能量的数量

        ##单局游戏内，假如返回了主菜单，还能继续游戏
        ##需要保存单局游戏的剩余时间，异种能量数目，经验数目，等级，角色属性加成情况，角色武器持有，角色技能冷却时间