import pygame 
from pygame.locals import *
import sys


class Button():

    def __init__(self):

        ##load photoshoped image of button 
        self.image = pygame.image.load('Button_Close.png')
        ##create the font for button 
        self.myfont = pygame.font.SysFont("Lucida Sans Unicode", 20)
        ##create text, colour 
        self.label = self.myfont.render("CLOSE", 1, (255,255,255))

    def buttonFont(self,screen): 
       self.image.blit(self.label, (30,5))
       screen.blit(self.image, (0,0))

       image = pygame.Surface([100,25], pygame.SRCALPHA, 32)
       image = image.convert_alpha()

##    def buttonMotion():
##        if event.type == pygame.MOUSEMOTION:
##            if(x in range(100,25)) and ( y in range(100,25)):
##                print "This will close the program"
       
                                         
pygame.init()

screen = pygame.display.set_mode((100, 25))
 
pygame.display.set_caption('Close Button')

button = Button()

while True :
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    
    button.buttonFont(screen)
    pygame.display.update()


            
        
        
    
