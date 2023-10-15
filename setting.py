import pygame
pygame.init()
class Settings():
    def __init__(self):
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        self.small_screen_width= self.screen_width // 1.2
        self.small_screen_height= self.screen_height // 1.2
        self.bg_color = (230, 230, 230)
        self.small_bg_color=(100,100,100)
    def save(self,energy,talents,status): #talents,status用字典传进来
        # 不知道写啥，快点告诉我保存什么
        #把你们要保存的写在这里

        ##天赋界面的提升情况
        ##纯粹能量的数量

        ##单局游戏内，假如返回了主菜单，还能继续游戏
        ##需要保存单局游戏的剩余时间，异种能量数目，经验数目，等级，角色属性加成情况，角色武器持有，角色技能冷却时间
        self.energy=energy
        self.talents=talents
        self.status={
            "time_left":0,
            "energy":0,
            "exp":0,
            "Lv":0,
            "stats":0, #这个传进来字典,人物属性啥的
            "weapon":"axe",
            "CD":0#每个技能冷却时间剩多少
        }
        #上面这个我会注释掉，你们按照这个格式传进来和读取
        self.status = dict(status) #然后传的时候不要直接=，不然 python 会自动&取地址，然后存档就寄了


