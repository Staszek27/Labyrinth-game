import pygame, sys,os
from          random import *
from           const import *

class Item:
    def __init__(self, pos, img, func_name, func_details):   
        self.x            = pos[0]
        self.y            = pos[1]
        self.img          = img
        self.func_name    = func_name
        self.func_details = func_details
    
    def __copy__(self):
        return Item((self.x, self.y), self.img, self.func_name, self.func_details)
        
    def draw_item(self):
        screen.blit(self.img, (self.x, self.y))
    
    def item_pos(self):
        return (self.x, self.y)
    
    def change_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
