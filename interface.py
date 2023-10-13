from button import Button
import sys
class Gamestatus():
    def __init__(self,screen,ai_settings) -> None:
        self.ai_settings=ai_settings
        self.screen=screen
        self.reset_stats()
    def reset_stats(self):
        # self.ship_left=self.ai_settings.ship_limit
        self.game_start=0
        self.pause=0
        # self.easy=1
        self.page=0
        self.score=0
        # self.reward=0
    def create_button(self,msg,width=150,height=50,size=48,FILLED=True):
        return Button(self.ai_settings,self.screen,msg,width,height,size,FILLED)
    def new_button(self,msg,centerx,centery,FILL=True):
        b=self.create_button(msg)
        b.rect.center=(centerx,centery)
        b.draw_button(FILL)
        return b
    def draw_page(self):
        if self.page==0:
            # pass
            # life=Life(self.screen)
            # life.draw_life(self.ship_left)

            # score_button=self.create_button("score:"+str(self.score),200,50,48,0)
            # score_button.rect.center=(self.ai_settings.screen_width-score_button.rect.width,float(score_button.rect.height)/2)
            # score_button.draw_button(False)
            self.start_button=self.new_button("Start",100,50)
            self.talent_button=self.new_button("Talent",100,150)
            self.config_button=self.new_button("Config",100,250)
            self.save_button=self.new_button("Save",100,350)
            self.quit_button=self.new_button("quit",100,450)
        elif self.page==1:
            self.back_button=self.new_button("Back",100,50)
        elif self.page==2:
            self.back_button=self.new_button("Back",100,50)
        elif self.page==3:
            self.back_button=self.new_button("Back",100,50)
        elif self.page==4:
            self.back_button=self.new_button("Back",100,50)
        
    def turn_page(self,mouse_x,mouse_y):
        if self.page==0:
            if self.start_button.rect.collidepoint(mouse_x,mouse_y):
                self.page=1
                self.game_start=1
            elif self.talent_button.rect.collidepoint(mouse_x,mouse_y):
                self.page=2
            elif self.config_button.rect.collidepoint(mouse_x,mouse_y):
                self.page=3
            elif self.save_button.rect.collidepoint(mouse_x,mouse_y):
                self.page=4
            if self.quit_button.rect.collidepoint(mouse_x,mouse_y):
                sys.exit()
        elif self.page==1:
            if self.back_button.rect.collidepoint(mouse_x,mouse_y):
                self.page=0
        elif self.page==2:
            if self.back_button.rect.collidepoint(mouse_x,mouse_y):
                self.page=0
        elif self.page==3:
            if self.back_button.rect.collidepoint(mouse_x,mouse_y):
                self.page=0
        elif self.page==4:
            if self.back_button.rect.collidepoint(mouse_x,mouse_y):
                self.page=0
        
            
            
        # elif self.page==1:
        #     if self.easy_rect.collidepoint(mouse_x,mouse_y):
        #         self.easy=1
        #         self.page+=1
        #     elif self.hard_rect.collidepoint(mouse_x,mouse_y):
        #         self.easy=0
        #         self.page+=1
        

        # if self.page==2:
        #     self.game_over=0
            
            

