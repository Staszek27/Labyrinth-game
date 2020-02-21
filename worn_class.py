import pygame, sys,os
from          random import *
from           const import *
from      item_class import *
from        eq_class import *

class Worn_items(Equipment):
    def __init__(self, items, img, slots):
        self.free_slots = set([i for i in range(len(items), slots)])
        self.items      = [self.set_item_pos(i, items[i]) for i in range(len(items))]
        self.it         = 0         
        self.img        = img  
        self.slots      = slots
        while len(self.items) < slots:
            self.items.append(self.set_item_pos(len(self.items), Item((0, 0), room_img, (), ())))       
        
    def set_item_pos(self, numb, item):
        y = numb * (mob_size + 3 * item_blank_size) + item_blank_size + board_size[1] / 3
        x = board_size[0] - move_size - 2 * item_blank_size
        item.change_pos((x, y))
        return item
    
    def it_pos(self):
        return (board_size[0] - 2 * move_size - 3 * item_blank_size,
                self.it * (mob_size + 3 * item_blank_size) + item_blank_size + board_size[1] / 3)
                

