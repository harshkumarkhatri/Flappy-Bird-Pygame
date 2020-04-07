import pygame
from pygame.mask import from_surface
import neat
import time
import os
import random

#loading images and setting thee screen
WIN_WIDTH=500
WIN_HEIGHT=800

BIRD_IMAGES=[pygame.transform.scale2x(pygame.image.load(os.path.join("images-fb","bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("images-fb","bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("images-fb","bird3.png")))]

PIPE_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("images-fb","pipe.png")))
BASE_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("images-fb","base.png")))
BG_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("images-fb","bg.png")))


class Bird:
    IMGS=BIRD_IMAGES
    # when we want to tilt the bird up and down it nose pointing that way.
    MAX_ROTATION=25
    # rotingn frames each time we want to move teh bird
    ROT_VEL=20
    # how long we show each bird animation
    ANIMATION_TIME=5
    def __init__(self,x,y):
        #def __int__(self,x,y):
        self.x=x
        self.y=y
        # deciding how much the image is tilting
        self.tilt=0
        # Deciding the physics of our bird when we jump or we g down
        self.tick_count=0
        # our velocity
        self.vel=0
        # deciding the height of the bord
        self.height=self.y
        # deciding the amount of images of the bird being displayed
        self.image_count=0
        # setting the initial image of the bird as the first one.
        self.img=self.IMGS[0]

    # setting a function which will be useful when we will jump
    def jump(self):
        # the inital velocity for our bird which will be ini upwards direction
        self.vel = -10.5
        # deciding how many times the bird will jump.Initial will be zero
        self.tick_count=0
        # initial height for the bird jump
        self.height=self.y

    #calling this method to move the frames in our game
    def move(self):
        # a tick happend and we jumped once
        self.tick_count+=1
        # displacement, this will be the distance our bird will be moving with each jump.
        # This will keep decreasing with each jump.
        d=self.vel*(self.tick_count)+1.5*self.tick_count**2

        # limiting thee move down vel to 16 if it is more.
        if d>=16:
            d=16

        # setting the jump up vel to be more than we get from above
        if d<0:
            d-=2

        # setting the y post of the bord.
        self.y=self.y+d

        # checking if we are moving above and tilting
        # the bird only when it has stopped moving up and begun to retrace back down.
        if d<0 or (self.y<(self.height+50)):

            # making sure the bird is not tilted the wrong way.
            # also checking where to tilt the bird (up or down)
            if self.tilt<self.MAX_ROTATION:
                self.tilt=self.MAX_ROTATION
            else:

                # rotating the bord completely downwards
                if self.tilt>-90:
                    self.tilt=self.ROT_VEL

    # win represents the window on which we draw the bord.
    def draw(self,win):
        # tracking how many times we have shown the image.
        self.image_count+=1

        # checking what image of the bord to be shown at what time
        if self.image_count<self.ANIMATION_TIME:
            self.img=self.IMGS[0]
        elif self.image_count<self.ANIMATION_TIME*2:
            self.img=self.IMGS[1]
        elif self.image_count<self.ANIMATION_TIME*3:
            self.img=self.IMGS[2]
        elif self.image_count<self.ANIMATION_TIME*4:
            self.img=self.IMGS[1]
        elif self.image_count == self.ANIMATION_TIME*4+1:
            self.img=self.IMGS[0]
            self.image_count = 0

        # checking if the bird going sown then setting the image acc.
        if self.tilt<= -80:
            self.img=self.IMGS[1]

            # making the bird to not skip a frame when it goes back up again.
            self.image_count=self.ANIMATION_TIME*2

        # rotating the image about its center
        rotated_image=pygame.transform.rotate(self.img,self.tilt)
        # moving the bord also after the rotation to avoid looking weird
        new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)

        # drawing the image on win
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return from_surface(self.img)


#6:10


# drawing the stuff
def draw_window(win,bird):
    # drawing the background image
    win.blit(BG_IMAGE,(0,0))
    # drawing the bord along with the tilt and rotations
    bird.draw(win)
    # updating the display
    pygame.display.update()


def main():
    bird=Bird(200,400)
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    # Setting the time to slow if we we want bird to fall down slowly
    clock=pygame.time.Clock()

    # variable to be changed to stop
    run=True

    # this will be helpful in running.
    while run:

        # slowing the clock
        clock.tick(30)

        # checking for an event
        for event in pygame.event.get():
            # for closing the game
            if event.type==pygame.QUIT:
                run=False

        # moving the bird
        bird.move()

        # drawing the bird
        draw_window(win,bird)

    pygame.quit()
    quit()

main()