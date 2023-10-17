from button import Button
from setting import Settings
import pygame
import sys

chara=[]
name=["lwt","lwt","lwt"]

chara.append (pygame.image.load('character\character1\char.bmp'))
chara.append (pygame.image.load('character\character1\char2.png'))
chara.append (pygame.image.load('character\character1\char1.png'))

class Gamestatus():
    def __init__(self,screen,ai_settings) -> None:
        self.ai_settings=ai_settings
        self.screen=screen
        self.reset_stats()
    def reset_stats(self):
        self.game_start=0
        self.game_over=0
        self.enemy=[]
        self.chara=None
        self.person_id=0
        self.game_lose=0
        self.bao=0
        self.pause=0
        self.easy=1
        self.page=0
        self.score=0
        self.time=0
        # self.reward=0
    def create_button(self,msg,width=150,height=50,size=48,FILLED=True,color=(0,255,0),img=None):
        return Button(self.ai_settings,self.screen,msg,width,height,size,FILLED,color,img)
    def new_button(self,msg,centerx,centery,width=150,height=50,color=(0,255,0),FILL=True):
        b=self.create_button(msg,width,height,48,True,color)
        b.rect.center=(centerx,centery)
        b.draw_button(FILL)
        return b
    def check_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y=pygame.mouse.get_pos()
                self.turn_page(mouse_x,mouse_y)
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                self.pause^=1
                if self.pause==1:
                    self.bao=1



    def create_person(self,centerx,ID):
        b=self.create_button("",150,400,0,True,(255,255,0),chara[ID])
        b.rect.center=(centerx,300)
        b.draw_button()
        b_name=self.create_button(name[ID],150,50,48,True,(0,255,0))
        b_name.rect.center=(centerx,600)
        b_name.draw_button()
        return b

    def show_game_statement(self):
        if self.game_start==0 or self.pause:return
        for enemy in self.enemy:
            self.hp_button=self.new_button("",enemy.rect.centerx,enemy.rect.centery-100,enemy.hp*10,30,(255,0,0))
        if self.chara != None:
            self.hp_button=self.new_button("",self.chara.rect.centerx,self.chara.rect.centery-100,self.chara.hp,30)
            self.level_button=self.create_button("level:"+str(self.chara.level),200,50,48,0)
            self.level_button.rect.center=(self.chara.rect.centerx,self.chara.rect.centery-130)
            self.level_button.draw_button(False)


        score_button=self.create_button("score:"+str(self.score),200,50,48,0)
        score_button.rect.center=(self.ai_settings.screen_width-score_button.rect.width,float(score_button.rect.height)/2)
        score_button.draw_button(False)

        time_button=self.create_button("time:"+str(self.time),200,50,48,0)
        time_button.rect.center=(score_button.rect.width,float(time_button.rect.height)/2)
        time_button.draw_button(False)

    def draw_page(self):
        if self.game_over==1:
            if self.game_lose:
                self.new_button("You lose",750,400)
            else :
                self.new_button("You win",750,400)

        if self.page==0:#初始
            # pass
            # life=Life(self.screen)

            # score_button=self.create_button("score:"+str(self.score),200,50,48,0)
            # score_button.rect.center=(self.ai_settings.screen_width-score_button.rect.width,float(score_button.rect.height)/2)
            # score_button.draw_button(False)
            self.start_button=self.new_button("Start",100,50)
            self.talent_button=self.new_button("Talent",100,150)
            self.config_button=self.new_button("Config",100,250)
            self.save_button=self.new_button("Save",100,350)
            self.quit_button=self.new_button("quit",100,450)

        elif self.page==1:#选人
            self.back_button=self.new_button("Back",100,50)
            self.p1_button=self.create_person(200,0)
            self.p2_button=self.create_person(600,1)
            self.p3_button=self.create_person(1000,2)
            
        elif self.page==2:#天赋
            self.back_button=self.new_button("Back",100,50)

        elif self.page==3:#设定
            self.back_button=self.new_button("Back",100,50)

        elif self.page==4:#存档
            self.back_button=self.new_button("Back",100,50)

        elif self.page==11:#难度
            self.back_button=self.new_button("Back",100,50)
            self.easy_button=self.new_button("easy",400,400)
            self.hard_button=self.new_button("hard",800,400)
            
            
    def show_other(self):
        if self.pause==1:#暂停选择返回主界面
            self.small_screen=self.create_button("",self.ai_settings.small_screen_width,self.ai_settings.small_screen_height,0,True,color=(255,255,255))
            self.small_screen.rect.center=(self.ai_settings.screen_width/2,self.ai_settings.screen_height/2)
            self.small_screen.draw_button()
            self.menu_button=self.new_button("Menu",600,600)
        elif self.pause==2:##进入单局游戏内三选一提升
            self.small_screen=self.create_button("",self.ai_settings.small_screen_width,self.ai_settings.small_screen_height,0,True,color=(255,255,255))
            self.small_screen.rect.center=(self.ai_settings.screen_width/2,self.ai_settings.screen_height/2)
            self.small_screen.draw_button()
            self.talent_button_1=self.new_button("talent1",383,444)
            self.talent_button_2=self.new_button("talent2",683,444)
            self.talent_button_3=self.new_button("talent3",1083,444)


    def colli(self,bt):
        return bt.rect.collidepoint(self.mouse_x,self.mouse_y)
    def turn_page(self,mouse_x,mouse_y):
        self.mouse_x=mouse_x
        self.mouse_y=mouse_y
        if self.pause==1:#暂停
            if self.colli(self.menu_button):
                self.game_start=0
                self.page=0
                self.pause=0
            return
        
        if self.pause == 2:##升级界面
            if self.colli(self.talent_button_1):
                ##把选项1传入到人物属性提升
                self.pause = 0
            elif self.colli(self.talent_button_2):
                self.pause = 0
            elif self.colli(self.talent_button_3):
                self.pause = 0
            return
        
        if self.page==0:#初始界面
            if self.colli(self.start_button):
                self.page=1
            elif self.colli(self.talent_button):
                self.page=2
            elif self.colli(self.config_button):
                self.page=3
            elif self.colli(self.save_button):
                self.page=4
            if self.colli(self.quit_button):
                sys.exit()

        elif self.page==1:#选人
            if self.colli(self.back_button):
                self.page=0
            elif self.colli(self.p1_button):
                self.page=11
                self.person_id=1
            elif self.colli(self.p2_button):
                self.page=11
                self.person_id=2
            elif self.colli(self.p3_button):
                self.page=11    
                self.person_id=3

        elif self.page==2:#天赋
            if self.colli(self.back_button):
                self.page=0

        elif self.page==3:#设定
            if self.colli(self.back_button):
                self.page=0

        elif self.page==4:#存档
            if self.colli(self.back_button):
                self.page=0

        elif self.page==11:#难度
            if self.colli(self.back_button):
                self.page=1
            if self.colli(self.easy_button):
                self.easy=1
                self.page=111
                self.game_start=1
            if self.colli(self.hard_button):
                self.easy=0
                self.page=111
                self.game_start=1
            
            
            

