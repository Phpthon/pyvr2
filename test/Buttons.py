import pygame 
from pygame.locals import *
import sys


class Button(pygame.Surface):

    def __init__(self):

        pygame.Surface.__init__(self, size = (100,50))
        self.hovered = False

        button = pygame.image.load("buttoncloseNew.png")
        self.state_normal = button.subsurface((0,0,100,25))
        self.state_hover = button.subsurface((0,25,100,25))
        self.myfont = pygame.font.SysFont("Lucida Sans Unicode", 20) 
        self.label = self.myfont.render("CLOSE", 1, (142,142,142))

    def update(self,screen):
        self.process_events()
        self.fill((0,0,0))

        newimage = self.get_image()
        self.blit(newimage, newimage.get_rect())
        self.blit(self.label, (30,5))

        screen.blit(self, self.get_rect())
        
    def buttonMotion():
        if event.type == pygame.MOUSEMOTION:
                print "This will close the program"

    def get_image(self):
        if self.hovered:
            return self.state_hover
        else:
            return self.state_normal

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if self.get_rect().collidepoint(event.pos):
                        self.hovered = True         
                else:   
                    self.hovered = False
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit 
       
                                         
pygame.init()

screen = pygame.display.set_mode((200, 200))
 
pygame.display.set_caption('Close Button')

button = Button()
clock = pygame.time.Clock()

while True :
    button.update(screen)
    pygame.display.update()
    clock.tick(30)
                                              





            
        
        
    
