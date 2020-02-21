import pygame, sys,os
from             random import *
from           const import *
from       mob_class import *

class Human(Mobs):
    def show_hp(self):
        pos = (board_size[0] - move_size - item_blank_size, board_size[1] - move_size - item_blank_size)
        for  i in range(self.max_hp):
            if self.max_hp - i > self.hp:
                screen.blit(empty_live_img, pos)
            else:
                screen.blit(full_live_img, pos)
            pos = (pos[0] - move_size, pos[1])
    
    def show_parameters(self): 
        show_text('STATS: ',                                     yellow, (board_size[0] - 70, board_size[1] - 99))
        show_text('ATT: ' + str(self.attack),                     white, (board_size[0] - 70, board_size[1] - 83))
        show_text('ACC: ' + str(int(self.accuracy * 100)) + ' %', white, (board_size[0] - 70, board_size[1] - 70))
        show_text('DEF: ' + str(self.defence),                    white, (board_size[0] - 70, board_size[1] - 57))
        
