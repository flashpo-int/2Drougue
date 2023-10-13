import pygame.font
class Button():
    def __init__(self,ai_settings,screen,msg,width=200,height=50,size=48,FILLED=True) -> None:
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.ai_settings=ai_settings
        self.width,self.height=width,height
        self.button_color=(0,255,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,size)
        
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center
        self.prep_msg(msg,FILLED)
    def prep_msg(self,msg,FILLED):
        if FILLED:
           self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        else :
            self.msg_image=self.font.render(msg,True,self.text_color,self.ai_settings.bg_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center
    def draw_button(self,FIllED=True):
        self.msg_image_rect.center=self.rect.center
        if FIllED:
            self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)