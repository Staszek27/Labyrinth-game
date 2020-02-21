import pygame, sys,os
from          random import *
from           const import *
from      item_class import *

class Equipment:
    def __init__(self, items, img, slots):
        self.free_slots = set([i for i in range(len(items), slots)])
        self.items      = [self.set_item_pos(i, items[i]) for i in range(len(items))]
        self.it         = 0
        self.img        = img
        self.slots      = slots
        while len(self.items) < self.slots:
            self.items.append(self.set_item_pos(len(self.items), Item((0, 0), room_img, (), ())))       
    
    def set_item_pos(self, numb, item):
        x = numb * (mob_size + 3 * item_blank_size) + item_blank_size
        y = board_size[1] - move_size - 2 * item_blank_size
        item.change_pos((x, y))
        return item
    
    def it_pos(self):
        return (self.it * (mob_size + 3 * item_blank_size) + item_blank_size,
                board_size[1] - 2 * move_size - 3 * item_blank_size)
                
    def show_eq(self): 
        screen.blit(self.img, self.it_pos())
        for e in self.items:
            pygame.draw.rect(screen, white, (e.item_pos()[0] - item_blank_size, 
                                             e.item_pos()[1] - item_blank_size, 
                                             item_blank_size * 2 + mob_size, 
                                             item_blank_size * 2 + mob_size))
            e.draw_item()
    
    def add_item(self, item):
        if len(self.free_slots) == 0:
            print('no empty slots')
        else:
            my_elem          = sorted(list(self.free_slots))[0]
            self.items[my_elem] = self.set_item_pos(my_elem, item)
            self.free_slots -= set([my_elem])        
    
    def delete_item_from_it(self, x):
        self.free_slots.add(x)
        self.items[x] = self.set_item_pos(x, Item((0, 0), room_img, (), ()))
        
    def delete_item(self):
        if not self.it in self.free_slots:
            self.free_slots.add(self.it)
            self.items[self.it] = self.set_item_pos(self.it, Item((0, 0), room_img, (), ()))
    
    def curr_item(self):
        return self.items[self.it]
    
    def it_on_item(self):
        if self.it in self.free_slots:
            return False
        return True
        
    def inc_it(self):
        self.it = min(self.slots - 1, self.it + 1)
        
    def dec_it(self):
        self.it = max(0,              self.it - 1)        
