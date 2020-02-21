import pygame, sys,os
from          random import *

# constants
move_size  = mob_size = 32
board_size            = (800, 600)
time_delay            = 10
rooms_density         = 50
rooms_length          = 10
sight_range           = 100
item_blank_size       = 4  
mob_move_range        = sight_range * 2 
mob_blocks_human      = False
font_details          = ('comicsansms', 20)
coms_time_delay       = 50
mob_tick              = 10
lanterns_amount       = 2

# interface setup
window = pygame.display.set_mode(board_size)
screen = pygame.display.get_surface()
clock  = pygame.time.Clock()

# load some images
win_img        = pygame.image.load('images/win_img.png')
lose_img       = pygame.image.load('images/lose_img.png')
the_end_img    = pygame.image.load('images/doors_img.png')
armour2_img    = pygame.image.load('images/armour2_img.png')
armour1_img    = pygame.image.load('images/armour1_img.png')
lantern_img    = pygame.image.load('images/lantern_img.png')
dmg_img        = pygame.image.load('images/dmg_img.jpg')
heal_img       = pygame.image.load('images/heal_img.jpg')
block_img      = pygame.image.load('images/block_img.jpg')
hp_block2_img  = pygame.image.load('images/no_hp.png')
hp_block1_img  = pygame.image.load('images/hp.jpg')
mob2_img       = pygame.image.load('images/spider.jpg')
mob_img        = pygame.image.load('images/monster1.jpg')
it_img         = pygame.image.load('images/it.png')
it2_img        = pygame.image.load('images/it_2.png')
empty_live_img = pygame.image.load('images/live2.png')
full_live_img  = pygame.image.load('images/live1.png')
black_img      = pygame.image.load('images/forest.jpg')
human_img      = pygame.image.load('images/human.jpg')
room_img       = pygame.image.load('images/room.jpg')
blank_img      = pygame.image.load('images/blank.jpg')
sword1_img     = pygame.image.load('images/sword1.jpg')
sword2_img     = pygame.image.load('images/sword2.jpg')
axe1_img       = pygame.image.load('images/axe1.jpg')
axe2_img       = pygame.image.load('images/axe2.jpg')
small_pot_img  = pygame.image.load('images/potion1.jpg')
medium_pot_img = pygame.image.load('images/potion2.jpg')

# basic RGB colors
black   = (  0,   0,   0)
white   = (255, 255, 255)
green   = (  0, 255,   0)
red     = (255,   0,   0)
blue    = (  0,   0, 255)
brown   = (165,  42,  42)
pink    = (255, 110, 180)
magenta = (255,   0, 255) 
yellow  = (255, 255,   0)

# useful functions
def copy_list(x):
    return [e for e in x]
    
def dist(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def random_action(chance):
    if randint(0, 1000000000) < chance * 1000000000:
        return True
    return False

def show_text(message, color, pos):
    font = pygame.font.SysFont(font_details[0], font_details[1])
    text = font.render(message, 1, color)
    screen.blit(text, pos)

