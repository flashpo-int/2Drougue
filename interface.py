from button import Button
from setting import Settings
import pygame
from random import randint
import sys

import numpy as np
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volRange=volume.GetVolumeRange()
volBar=400
volPer=0
print(volRange)
minVol=volRange[0]
maxVol=volRange[1]

chara=[]
name=["lwt","lwt","lwt"]

chara.append (pygame.image.load('character\character1\charrest.png'))
chara.append (pygame.image.load('character\character1\charrest.png'))
chara.append (pygame.image.load('character\character1\charrest.png'))

talent=["hp_up","shield_up","dmg_bonus","crit_rate","crit_dmg","miss"]
buff=[0,0,0]
level=[0,0,0]
start=pygame.image.load('background\start.png')
start=pygame.transform.smoothscale(start,(150,50))

bg=pygame.image.load('background\主界面.jpg')
bg=pygame.transform.smoothscale(bg,(1500,800))

class Gamestatus():
    def __init__(self,screen,ai_settings) -> None:
        self.ai_settings=ai_settings
        self.screen=screen
        self.vol = volume.GetMasterVolumeLevelScalar()
        self.vol=np.interp(self.vol,[0.0,1.0],[minVol,maxVol])
        self.volPer=np.interp(self.vol,[minVol,maxVol],[0,100])
        self.reset_stats()
    def reset_stats(self):
        self.game_start=0
        self.restart=0
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
        self.chara_pre_level=0
        self.volume_left=550
        self.volume_right=1050
        # self.reward=0
    def create_button(self,msg,width=150,height=50,size=48,FILLED=True,color=(0,255,0),img=None):
        return Button(self.ai_settings,self.screen,msg,width,height,size,FILLED,color,img)
    def new_button(self,msg,centerx,centery,width=150,height=50,color=(0,255,0),img=None):
        b=self.create_button(msg,width,height,48,True,color,img)
        b.rect.center=(centerx,centery)
        b.draw_button(True)
        return b
    def check_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y=pygame.mouse.get_pos()
                self.turn_page(mouse_x,mouse_y)
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                if self.pause==2 or self.pause==3:return
                self.pause^=1
                if self.pause==1:
                    self.bao=1



    def create_person(self,centerx,ID):
        b=self.create_button("",150,400,0,True,(255,255,0),chara[ID])
        b.rect.center=(centerx,300)
        b.draw_button()
        b2=self.new_button(name[ID],centerx,600,150,50,(0,0,0),start)
        return b,b2

    def reget_buff(self):
        level[0]=randint(1,3)
        level[1]=randint(1,3)
        level[2]=randint(1,3)
        buff[0]=randint(0,5)
        while buff[1]==buff[0]:buff[1]=randint(0,5)
        while buff[1]==buff[2] or buff[0]==buff[2]:buff[2]=randint(0,5)

    def show_game_statement(self):
        if self.game_start==0 or self.pause:return
        for enemy in self.enemy:
            self.hp_button=self.new_button("",enemy.rect.centerx,enemy.rect.centery-100,enemy.hp*10,10,(255,0,0))
        if self.chara != None:
            self.hp_button=self.new_button("",self.chara.rect.centerx,self.chara.rect.centery-90,self.chara.hp,15)
            self.shield_button=self.new_button("",self.chara.rect.centerx,self.chara.rect.centery-80,2.0*self.chara.shield,5,(0,0,255))
            self.level_button=self.create_button("level:"+str(self.chara.level),200,50,48,0)
            self.level_button.rect.center=(self.chara.rect.centerx,self.chara.rect.centery-130)
            self.level_button.draw_button(False)
            


        score_button=self.create_button("score:"+str(self.score),200,50,48,0)
        score_button.rect.center=(self.ai_settings.screen_width[self.ai_settings.screen_type]-score_button.rect.width,float(score_button.rect.height)/2)
        score_button.draw_button(False)

        time_button=self.create_button("time:"+str(self.time),200,50,48,0)
        time_button.rect.center=(score_button.rect.width,float(time_button.rect.height)/2)
        time_button.draw_button(False)
        if self.chara_pre_level!=self.chara.level:
            self.pause=2
            self.bao=1
            self.chara_pre_level=self.chara.level

    def draw_page(self):
        if self.game_start==1:return
        self.new_button("",750,400,1500,800,(0,0,0),bg)
        if self.page==0:#初始
            # pass
            # life=Life(self.screen)

            # score_button=self.create_button("score:"+str(self.score),200,50,48,0)
            # score_button.rect.center=(self.ai_settings.screen_width-score_button.rect.width,float(score_button.rect.height)/2)
            # score_button.draw_button(False)
            self.start_button=self.new_button("Start",100,50,150,50,(0,0,0),start)
            self.talent_button=self.new_button("Talent",100,150,150,50,(0,0,0),start)
            self.config_button=self.new_button("Config",100,250,150,50,(0,0,0),start)
            self.save_button=self.new_button("Save",100,350,150,50,(0,0,0),start)
            self.quit_button=self.new_button("quit",100,450,150,50,(0,0,0),start)

        elif self.page==1:#选人
            self.back_button=self.new_button("Back",100,50,150,50,(0,0,0),start)
            self.p1_button,self.p1_name_button=self.create_person(200,0)
            self.p2_button,self.p2_name_button=self.create_person(600,1)
            self.p3_button,self.p3_name_button=self.create_person(1000,2)
            
        elif self.page==2:#天赋
            self.back_button=self.new_button("Back",100,50,150,50,(0,0,0),start)

        elif self.page==3:#设定
            self.back_button=self.new_button("Back",100,50,150,50,(0,0,0),start)
            volume=self.create_button("volume",200,50,48,0)
            volume.rect.center=(300,500)
            volume.draw_button(False)
            self.volume_button=self.new_button("",(self.volume_left+self.volume_right)/2,500,self.volume_right-self.volume_left,30,(191,98,10))
            self.volume_pos=np.interp(self.vol,[minVol,maxVol],[self.volume_left,self.volume_right])
            self.new_button("",self.volume_pos,500,40,70,(114,51,4))
            Per=self.create_button(str(int(self.volPer))+"%",200,50,48,0)
            Per.rect.center=(self.volume_right+50,500)
            Per.draw_button(False)

        elif self.page==4:#存档
            self.back_button=self.new_button("Back",100,50,150,50,(0,0,0),start)

        elif self.page==11:#难度
            self.back_button=self.new_button("Back",100,50,150,50,(0,0,0),start)
            self.easy_button=self.new_button("easy",400,400,150,50,(0,0,0),start)
            self.hard_button=self.new_button("hard",800,400,150,50,(0,0,0),start)
            
            
    def show_other(self):
        if self.pause==1:#暂停选择返回主界面
            self.small_screen=self.create_button("",self.ai_settings.small_screen_width[self.ai_settings.screen_type],self.ai_settings.small_screen_height[self.ai_settings.screen_type],0,True,color=(255,255,255))
            self.small_screen.rect.center=(self.ai_settings.screen_width[self.ai_settings.screen_type]/2,self.ai_settings.screen_height[self.ai_settings.screen_type]/2)
            self.small_screen.draw_button()
            self.menu_button=self.new_button("Menu",900,600,150,50,(0,0,0),start)
            self.full_button=self.new_button("full",600,600,150,50,(0,0,0),start)
            self.back2_button=self.new_button("back",300,600,150,50,(0,0,0),start)
            volume=self.new_button("volume",300,500,150,50,(0,0,0),start)
            self.volume_button=self.new_button("",(self.volume_left+self.volume_right)/2,500,self.volume_right-self.volume_left,30,(191,98,10))
            self.volume_pos=np.interp(self.vol,[minVol,maxVol],[self.volume_left,self.volume_right])
            self.new_button("",self.volume_pos,500,40,70,(114,51,4))
            Per=self.create_button(str(int(self.volPer))+"%",200,50,48,0)
            Per.rect.center=(self.volume_right+50,500)
            Per.draw_button(False)
        elif self.pause==2:##进入单局游戏内三选一提升
            if buff[0]==buff[1]:
                self.reget_buff()
            self.talent_button_1=self.new_button(talent[buff[0]],383,444,150,50,(0,0,0),start)
            self.talent_button_2=self.new_button(talent[buff[1]],683,444,150,50,(0,0,0),start)
            self.talent_button_3=self.new_button(talent[buff[2]],1083,444,150,50,(0,0,0),start)
        elif self.pause==3:
            self.small_screen=self.create_button("",self.ai_settings.small_screen_width[self.ai_settings.screen_type],self.ai_settings.small_screen_height[self.ai_settings.screen_type],0,True,color=(255,255,255))
            self.small_screen.rect.center=(self.ai_settings.screen_width[self.ai_settings.screen_type]/2,self.ai_settings.screen_height[self.ai_settings.screen_type]/2)
            self.small_screen.draw_button()
            self.restart_button=self.new_button("restart",600,600,150,50,(0,0,0),start)
            score_button=self.create_button("score:"+str(self.score),200,50,48,0)
            score_button.rect.center=(300,450)
            score_button.draw_button(False)

            if self.game_lose==1:
                self.new_button("you lose",600,300,150,50,(0,0,0),start)
            else:
                self.new_button("you win",600,300,150,50,(0,0,0),start)
            
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
            elif self.colli(self.full_button):
                self.ai_settings.screen_type^=1
                self.screen=pygame.display.set_mode((self.ai_settings.screen_width[self.ai_settings.screen_type],self.ai_settings.screen_height[self.ai_settings.screen_type]))
            elif self.colli(self.volume_button):
                self.vol=np.interp(self.mouse_x,[self.volume_left,self.volume_right],[minVol,maxVol])
                self.volPer=np.interp(self.vol,[minVol,maxVol],[0,100])
                volume.SetMasterVolumeLevel(self.vol,None)
            elif self.colli(self.back2_button):
                self.pause=0
            return
        
        if self.pause == 2:##升级界面
            if self.colli(self.talent_button_1):
                self.chara.get_buff(buff[0]+1,level[0])
                buff[0]=buff[1]=0
                self.pause = 0
            elif self.colli(self.talent_button_2):
                self.chara.get_buff(buff[1]+1,level[1])
                buff[0]=buff[1]=0
                self.pause = 0
            elif self.colli(self.talent_button_3):
                self.chara.get_buff(buff[2]+1,level[2])
                buff[0]=buff[1]=0
                self.pause = 0
            return
        elif self.pause==3:
            if self.colli(self.restart_button):
                self.restart=1
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
            elif self.colli(self.p1_button) or self.colli(self.p1_name_button):
                self.page=11
                self.person_id=1
            elif self.colli(self.p2_button) or self.colli(self.p2_name_button):
                self.page=11
                self.person_id=2
            elif self.colli(self.p3_button) or self.colli(self.p3_name_button):
                self.page=11    
                self.person_id=3

        elif self.page==2:#天赋
            if self.colli(self.back_button):
                self.page=0

        elif self.page==3:#设定
            if self.colli(self.back_button):
                self.page=0
            elif self.colli(self.volume_button):
                self.vol=np.interp(self.mouse_x,[self.volume_left,self.volume_right],[minVol,maxVol])
                self.volPer=np.interp(self.vol,[minVol,maxVol],[0,100])
                volume.SetMasterVolumeLevel(self.vol,None)

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

            
            

