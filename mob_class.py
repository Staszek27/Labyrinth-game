import pygame, sys,os
from          random import *
from           const import *

class Mobs:
    def __init__(self, hp, pos, name, img, defence, attack, accuracy, thieving, speed):
        self.alive    = True
        self.max_hp   = hp
        self.hp       = hp
        self.x        = pos[0]
        self.y        = pos[1]
        self.name     = name
        self.img      = img
        self.defence  = defence
        self.attack   = attack
        self.accuracy = accuracy
        self.thieving = thieving
        self.speed    = speed
        self.texts    = [] # tick numb img
        
    def mob_pos(self):
        return (self.x, self.y)
        
    def move(self, g):
        self.x += g[0]
        self.y += g[1]
    
    def show_name(self):
        show_text(self.name, white, (self.x + 3, self.y + 20))
        
    def show_hp(self):
        hp_length = 5
        for i in range(1, hp_length + 1):
            if i == 1 or self.hp / self.max_hp + 0.0001 > i / hp_length:
                screen.blit(hp_block1_img, (self.x + (i - 1) * 5 + 3, self.y))
                continue
            screen.blit(hp_block2_img, (self.x + (i - 1) * 5 + 3, self.y))
    
    def update_texts(self, tick):
        new_list = []
        for e in self.texts:
            if e[0] + mob_tick > tick: 
                new_list.append(e)
        texts = [max(new_list)]
        
    def draw_mob(self, tick):
        # update texts   
        new_list = []
        for e in self.texts:    
            if tick <= e[0] + mob_tick: 
                new_list.append(e)
        self.texts = new_list
        
        screen.blit(self.img, (self.x, self.y))
        for e in self.texts:
            screen.blit(e[2], (self.x + 6, self.y + 6))
            if e[2] == heal_img:
                show_text(e[1], blue, (self.x + 12, self.y + 12))
            else:
                show_text(e[1], white, (self.x + 12, self.y + 12))
            
        self.show_hp()
        self.show_name()
                
    def change_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
  
    def heal(self, amount, tick):
        self.texts.append([tick, str(amount), heal_img])
        self.hp = min(self.max_hp, self.hp + amount)
        
    def hurt(self, amount, tick):
        if amount == 0:
            self.texts.append([tick, '0', block_img])
        else:
            self.texts.append([tick, str(amount), dmg_img])
            
        self.hp -= max(0, amount)
        if self.hp <= 0:
            self.alive = False
