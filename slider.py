import os,sys
import pygame as pg
import math
import time

class Character:

    slider_sprites = None

    def __init__(self, rect):

        if Character.slider_sprites == None:
            sprites = pg.image.load("slider-sprites.png")
            Character.slider_sprites = [
                sprites.subsurface((0,0,210,13)).copy(),
                sprites.subsurface((0,13,210,13)).copy(),
                sprites.subsurface((0,26,30,7)).copy(),
                sprites.subsurface((0,33,30,7)).copy()
            ]

        # user options
        self.paddingright = 3
        self.paddingleft = 3
        self.increment = 10
        self.minvalue = 10.0
        self.maxvalue = 100.0
        self.x, self.y = 35, 50

        # init the track
        self.track_rect = Character.slider_sprites[0].get_rect().copy()
        self.track_rect.x = self.x
        self.track_rect.y = self.y - 3

        # calc max start/end position of bar
        self.maxright = self.track_rect.right - self.paddingright
        self.maxleft = self.track_rect.x + self.paddingleft

        # init the bar
        self.bar_rect = Character.slider_sprites[2].get_rect().copy()
        self.bar_rect.x = self.maxleft
        self.bar_rect.y = self.y

        self.click = False
        self.offset = None
        self.currentvalue = 0

        # calculate empty space between bar and padded edges along with the ratio
        self.emptyspace = self.maxright - self.maxleft - self.bar_rect.width
        self.ratio = ((self.maxvalue - self.minvalue) / self.increment) / self.emptyspace

        self.track_image = Character.slider_sprites[0]
        self.bar_image = Character.slider_sprites[2]

        print self.emptyspace

    def _hovered(self, is_hovered):
        if is_hovered:
            self.track_image = Character.slider_sprites[1]
        else:
            self.track_image = Character.slider_sprites[0]


    def _hovered_bar(self, is_hovered):
        if is_hovered:
            self.bar_image = Character.slider_sprites[3]
        else:
            self.bar_image = Character.slider_sprites[2]

    def update(self,surface):
        if self.click:
            newpos = pg.mouse.get_pos()[0] - self.offset
            if newpos + self.bar_rect.width < self.maxright and newpos > self.maxleft:
                self.bar_rect.right = newpos + self.bar_rect.width
            elif newpos + self.bar_rect.width > self.maxright:
                self.bar_rect.right = self.maxright
            elif newpos < self.maxleft:
                self.bar_rect.left = self.maxleft
        font = pg.font.SysFont('Lucida Sans', 9)

        #print (self.bar_rect.right - self.maxright)
        #print self.maxright - self.bar_rect.right
        #print self.bar_rect.right - self.maxright + self.emptyspace

        self.currentvalue = self.myround( ( (self.bar_rect.right - self.maxright + self.emptyspace ) * self.ratio) * self.increment + self.minvalue, self.increment)
        text = font.render(str(self.currentvalue), True, (41, 140, 218))
        surface.blit(text, (self.bar_rect.center[0] - text.get_rect().width / 2, self.bar_rect.top - 15))
        Screen.blit(self.track_image, self.track_rect)
        Screen.blit(self.bar_image, self.bar_rect)

    def myround(self, x, base=5):
        return int(base * math.ceil(float(x)/base))

def main(Surface,Player):
    game_event_loop(Player)
    #Surface.fill(0)
    Player.update(Surface)
def game_event_loop(Player):
    for event in pg.event.get():
        if event.type == pg.MOUSEMOTION:
            if Player.track_rect.collidepoint(event.pos):
                Player._hovered(True)
            elif not Player.click:
                Player._hovered(False)
        if event.type == pg.MOUSEBUTTONDOWN:

            if Player.bar_rect.collidepoint(event.pos):
                Player._hovered_bar(True)
                Player.click = True
                if Player.offset is None:
                    Player.offset = pg.mouse.get_pos()[0] - Player.bar_rect.x

        elif event.type == pg.MOUSEBUTTONUP:
            Player.click = False
            Player.offset = None
            Player._hovered_bar(False)

        elif event.type == pg.QUIT:
            pg.quit(); sys.exit()

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    size = (300,300)
    Screen = pg.display.set_mode(size)
    MyClock = pg.time.Clock()
    timer = 0
    MyPlayer = Character((0,250,150,150))
    surf = pg.Surface((100, 300))
    MyPlayer.hover = surf
    #MyPlayer.rect.center = Screen.get_rect().center

    testing = pg.Surface((50,50))
    testing.fill((142,228,104))
    testrect = testing.get_rect()
    testrect.y = 150
    testrect.x = 50
    print testrect
    direction = 0
    counter = 0
    velocity = [1,1]
    x, y = 50, 150
    speed = 1

    while 1:
        seconds = timer / 1000.0

        Screen.fill((242, 242, 242))
        Screen.blit(testing, testrect)
        main(Screen,MyPlayer)
        
        #surf.fill((145,145,90))

        if testrect.bottom > size[1] - 5: velocity[1] = -1
        if testrect.top < 100: velocity[1] = 1
        if testrect.right > size[0] - 5: velocity[0] = -1
        if testrect.left < 5: velocity[0] = 1


        x += MyPlayer.currentvalue * velocity[0] * seconds
        y += MyPlayer.currentvalue * velocity[1] * seconds

        testrect.x = x
        testrect.y = y
        #Screen.blit(sprites, (300,300))

        #Screen.blit(clipped, (400,400))

        pg.display.update()
        timer = MyClock.tick(60)