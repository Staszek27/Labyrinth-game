import pygame, sys,os
from pygame.locals import *
import pygame, sys,os
from             labirynth_class import *


def main():
    # basic pygame methods
    pygame.init()
    pygame.display.set_caption('Labirynth by Michal Bryjak')
    
    
    # run a game
    game = Labirynth()
    game.run()
    
    
main()
