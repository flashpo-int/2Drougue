import pygame
pygame.init()
size_ratio = 10
# enemy size
enemy_width = 5*size_ratio
enemy_height = enemy_width*1.06

# character size
chara_width = 8*size_ratio
chara_height = chara_width*1.06

# weapon size
weapon_width = 5*size_ratio
weapon_height = weapon_width*0.27

# character image
enemy1 = pygame.image.load('character\enemy1\sprite1.png')
enemy1 = pygame.transform.smoothscale(enemy1, (enemy_width, enemy_height))
enemy2 = pygame.image.load('character\enemy2\sprite1.png')
enemy2 = pygame.transform.smoothscale(enemy2, (enemy_width, enemy_height))
enemy3 = pygame.image.load('character\enemy3\sprite1.png')
enemy3 = pygame.transform.smoothscale(enemy3, (enemy_width, enemy_height))
chara1 = pygame.image.load('character\character1\charrest.png')
chara1 = pygame.transform.smoothscale(chara1, (chara_width, chara_height))

# weapon image
arrow = pygame.image.load('weapon/arrow.png')
arrow = pygame.transform.smoothscale(arrow,(weapon_width,weapon_height))
bow = pygame.image.load('weapon/bow.png')
bow = pygame.transform.smoothscale(bow,(weapon_width,weapon_height))
knife = pygame.image.load('weapon/knife.png')
knife = pygame.transform.smoothscale(knife,(weapon_width,weapon_height))
shield = pygame.image.load('weapon/shield.png')

shield= pygame.transform.smoothscale(shield,(weapon_width,weapon_height))
sword = pygame.image.load('weapon/sword.png')
sword = pygame.transform.smoothscale(sword,(weapon_width,weapon_height))
# score
max_score = 1000

class Settings():
    def __init__(self):
        self.screen_info = pygame.display.Info()
        self.screen_width=[]
        self.screen_height=[]
        self.small_screen_width=[0,0]
        self.small_screen_height=[0,0]
        self.screen_width.append(self.screen_info.current_w)
        self.screen_height.append(self.screen_info.current_h)
        self.screen_width.append(1500)
        self.screen_height.append(800)
        self.screen_type=1
        for i in range(0,2):
            self.small_screen_width[i]= self.screen_width[i] // 1.2
            self.small_screen_height[i]= self.screen_height[i] // 1.2
        self.bg_color = (230, 230, 230)
        self.small_bg_color=(100,100,100)
        self.game_fps=60.0
        self.max_time=15*60
    def save(self,what):
        self.recod=what # 不知道写啥，快点告诉我保存什么
        #把你们要保存的写在这里

        ##天赋界面的提升情况
        ##纯粹能量的数量

        ##单局游戏内，假如返回了主菜单，还能继续游戏
        ##需要保存单局游戏的剩余时间，异种能量数目，经验数目，等级，角色属性加成情况，角色武器持有，角色技能冷却时间