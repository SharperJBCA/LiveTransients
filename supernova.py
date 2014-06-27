import pygame,random,sys,hackmain
from matplotlib import pyplot
import numpy as np
from astropy.coordinates import FK5
import astropy.units as u

def InterestingObj():
	data = np.loadtxt('Objects.txt')
	ra = data[:,0]
	dec = data[:,1]
	return ra, dec

data=hackmain.GetTransients()
ra,dec,mag,jd=data.GetData()


#Interesting Objects:
ra_i,dec_i = InterestingObj()

print ra_i,dec_i

pygame.init()
clock=pygame.time.Clock()
WIDTH=1000;HEIGHT=500;BLACK=(0,0,0)
screen=pygame.display.set_mode([WIDTH,HEIGHT])

background_image=pygame.image.load('background.png')
imagerect=background_image.get_rect()

background=pygame.Surface(screen.get_size())
background=background.convert()
pygame.mixer.init(44100,-16,2,2048)
effect=pygame.mixer.Sound('explosion-01.mp3')

def get_pixel(ra,dec):
    x=int(ra/360.0*1000)
    y=int((90-dec)/180.0*500)

    return x,y
    


def draw_circle(ra,dec,mag,colour):
    x,y=get_pixel(ra,dec)
    size=int(mag)#int(1/mag*250)
    pygame.draw.circle(screen,colour,(x,y),size)

def random_colour(min,max):
    red=random.randint(min,max)
    green=random.randint(min,max)
    blue=random.randint(min,max)
    colour=[red,green,blue]
    return colour

clock = pygame.time.Clock()
lasttime = 0
totalTime = 0
while True:

    for n in range(len(ra)):
        totalTime += clock.tick()

        clock.tick(5)
        screen.blit(background_image,imagerect)
        colour=random_colour(100,255)

	print totalTime, lasttime
	if totalTime > lasttime + 10000:
            print 'Update!'
            data.Update()
            ra,dec,mag,jd=data.GetData()
	    lasttime = totalTime
	    clearclock = clock.tick()

        draw_circle(ra[n],dec[n],mag[n],colour)

        #draw_circle(ra_i[0],dec_i[0],20,[0,255,255])
        #draw_circle(ra_i[1],dec_i[1],20,[0,255,255])

        effect.play()
        pygame.display.flip()
	
     
    screen.fill((0,0,0))

raw_input("Press a key")
sys.exit()
