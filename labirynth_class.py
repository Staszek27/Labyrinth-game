import pygame, sys,os
from          random import *
from           const import *
from      item_class import *
from        eq_class import *
from       mob_class import *
from     human_class import *
from      worn_class import *
from            time import sleep
class Labirynth:
    def __init__(self):
        self.win        = False
        self.tick       = 0
        self.coms       = []
        self.blocked    = []
        self.rooms      = self.gen_board()
        self.human      = self.gen_human()
        self.the_end    = self.rooms[len(self.rooms) - 1]
        self.mobs       = self.gen_mobs()
        self.items      = self.gen_items()
        self.eq         = self.gen_eq()
        self.worn_items = self.gen_worn_items()
        self.lanterns   = self.gen_lanterns()
        
    
    def rand_pos(self):
        max_x   = board_size[0] // mob_size - 3
        max_y   = board_size[1] // mob_size - 2
        
        return (randint(0, max_x - 1) * mob_size, randint(0, max_y - 1) * mob_size)
    
    def gen_mobs(self):
        my_mobs = [Mobs(5,  (0, 0), 'BAT',  mob2_img, 1, 1, 0.5, 0.0, 40),
                   Mobs(10, (0, 0), 'CAT',  mob_img,  3, 1, 0.2, 0.7, 20),
                   Mobs(20, (0, 0), 'BLA',  mob2_img, 5, 5, 0.5, 0.5, 10)]
        
        def find_trail():
            odw = [[False for i in range(2000)] for j in range(2000)]
            
            def DFS(x, y, ans):
                if (x, y) == self.the_end:
                    return ans
                if (x, y) != (0, 0):
                    ans.append((x, y))
                odw[x][y] = True
                for e in [(0, mob_size), (0, -mob_size), (mob_size, 0), (-mob_size, 0)]:
                    if (x + e[0], y + e[1]) in self.rooms:
                        if not odw[x + e[0]][y + e[1]]:
                            k = DFS(x + e[0], y + e[1], copy_list(ans)) 
                            if k != []:
                                return k
                return []
            
            return DFS(0, 0, [])
        
        t = find_trail()
        for i in range(1, len(my_mobs) + 1):
            next = min(max(i * (len(t) // (len(my_mobs))) - 1, 0), len(t) - 1)
            my_mobs[i - 1].change_pos(t[-1 + i * (len(t) // (len(my_mobs)))])
            self.blocked.append(t[-1 + i * (len(t) // (len(my_mobs)))])
        return my_mobs    
                            
    def gen_human(self):
        return Human(10,  self.rooms[0], '', human_img, 0, 1, 0.2, 0, 0)
        
    def gen_items(self):
        my_items = [Item((0, 0), sword1_img,     'accuracy', [0.4]), 
                    Item((0, 0), sword2_img,     'accuracy', [0.3]), 
                    Item((0, 0), axe1_img,       'attack',   [2]), 
                    Item((0, 0), axe2_img,       'attack',   [3]), 
                    Item((0, 0), armour1_img,    'defence',  [2]), 
                    Item((0, 0), armour2_img,    'defence',  [3]),
                    Item((0, 0), small_pot_img,  'heal',     [3]),
                    Item((0, 0), small_pot_img,  'heal',     [3]),
                    Item((0, 0), medium_pot_img, 'heal',     [6]),]
        
        for i in range(len(my_items)):
            while True:
                cand = choice(self.rooms)
                if not cand in self.blocked:
                    my_items[i].change_pos(cand)
                    self.blocked.append(cand)
                    break
                    
        return my_items            
    
    def gen_eq(self):
        return Equipment([], it_img, 8)
        
    def gen_worn_items(self):
        return Worn_items([], it2_img, 4)
    
    def gen_lanterns(self):
        res = []
        while len(res) < lanterns_amount:
            k = self.rand_pos()
            if not k in self.rooms and not k in res:
                res.append(k)
        return res
        
    def in_sight(self, pos):
        if dist(self.human.mob_pos(), pos) <= sight_range:
            return True
        for e in self.lanterns:
            if dist(e, pos) <= sight_range / 1.8:
                return True
        return False
            
    def gen_board(self): 
        max_x   = board_size[0] // mob_size - 3
        max_y   = board_size[1] // mob_size - 2
        grid    = [(i, j) for i in range(max_x) for j in range(max_y)]
        
        def walls_foo(pos):
            res = []
            for i in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                if pos in grid and (pos[0] + i[0], pos[1] + i[1]) in grid:
                    res.append((pos, (pos[0] + i[0], pos[1] + i[1])))
            return res

        start   = (0, 0)
        maze    = [start]
        walls   = set(walls_foo(start))
        while len(walls) > 0:
            H = choice(list(walls))
            if H[0] in maze and H[1] not in maze:
                maze.append(((H[0][0] + H[1][0]) // 2, (H[0][1] + H[1][1]) // 2))
                maze.append(H[1])
                walls |= set(walls_foo(H[1]))
            walls.remove(H)
        
        return [(e[0] * mob_size, e[1] * mob_size) for e in maze]
            
    def draw_board(self):
        screen.blit(black_img, (0, 0))
        
        # printing rooms, mobs and items
        for e in self.rooms:
            screen.blit(room_img, e)
        for e in self.items:
            e.draw_item()
        screen.blit(the_end_img, self.the_end)
        for e in self.mobs:
            e.draw_mob(self.tick)
        
        # sight effect
        human_pos = self.human.mob_pos()
        for i in range(0, board_size[0] + 1, mob_size // 2):
            for j in range(0, board_size[1], mob_size // 2):
                if not self.in_sight((i, j)):
                    screen.blit(blank_img, (i, j))
        
        # object always in sight
        self.human.draw_mob(self.tick)
        self.human.show_hp()
        for e in self.coms:
           if e[0] > self.tick:
               show_text(e[1][0], e[1][1], e[1][2])
               
        for e in self.lanterns:
           screen.blit(lantern_img, (e[0] + 5, e[1] + 5))
           
        self.eq.show_eq()
        self.worn_items.show_eq()
        self.human.show_parameters()
        pygame.display.update()
        
    
    def check_and_make_move(self, g):
        new_pos = (self.human.mob_pos()[0] + g[0], self.human.mob_pos()[1] + g[1])
        if new_pos in self.rooms:
            if not mob_blocks_human or not new_pos in [self.mobs[i].mob_pos() 
                                                       for i in range(len(self.mobs))]:
                self.human.move(g)
    
    def check_and_pick_item(self):
        if self.eq.free_slots == set():
            return
        new_item_list = []
        for e in self.items:
            if e.item_pos() == self.human.mob_pos():
                self.eq.add_item(e)
            else:
                new_item_list.append(e)
        self.items = new_item_list
    
    # humans' attacks depended on direction
    def human_attack(self, pos): 
        pos = (self.human.x + pos[0], self.human.y + pos[1])
        if pos in self.rooms:  
            for i in range(len(self.mobs)):
                if self.mobs[i].mob_pos() == pos:
                    if random_action(self.human.accuracy):
                        self.mobs[i].hurt(max(0, self.human.attack - self.mobs[i].defence), self.tick)
                    else:
                        self.mobs[i].hurt(0, self.tick)
    
    def use_curr_item(self):
        item = self.eq.curr_item()
        if   item.func_name == 'heal':
            self.human.heal(item.func_details[0], self.tick)
            self.eq.delete_item()
        elif self.worn_items.free_slots != set():   
            self.eq.delete_item()
            self.worn_items.add_item(item)
            if   item.func_name == 'attack':
                self.human.attack  += item.func_details[0]        
            elif item.func_name == 'defence':
                self.human.defence += item.func_details[0] 
            elif item.func_name == 'accuracy':
                self.human.accuracy = min(1.0, self.human.accuracy + item.func_details[0])
    
    def take_off(self):    
        item = self.worn_items.curr_item()       
        if   item.func_name == 'attack':
            self.human.attack  -= item.func_details[0]
        elif item.func_name == 'defence':  
            self.human.defence -= item.func_details[0]
        elif item.func_name == 'accuracy':
            self.human.accuracy = max(0.0, self.human.accuracy - item.func_details[0])
        self.eq.add_item(self.worn_items.curr_item())
        self.worn_items.delete_item()
    
    
    def make_action(self, keys):
        # Moving actions
        if   keys[pygame.K_w]:
            self.check_and_make_move((0, -move_size))
        elif keys[pygame.K_s]:
            self.check_and_make_move((0, move_size))
        elif keys[pygame.K_d]:
            self.check_and_make_move((move_size, 0))
        elif keys[pygame.K_a]:
            self.check_and_make_move((-move_size, 0))
        elif keys[pygame.K_e]:
            self.check_and_pick_item()
        elif keys[pygame.K_LEFTBRACKET]:
            self.eq.dec_it()
        elif keys[pygame.K_RIGHTBRACKET]:
            self.eq.inc_it()
        elif keys[pygame.K_EQUALS]:
            self.worn_items.inc_it()
        elif keys[pygame.K_MINUS]:
            self.worn_items.dec_it()
        elif keys[pygame.K_p]:
            if self.eq.it_on_item():
                self.items.append(self.eq.curr_item())
                self.items[len(self.items) - 1].change_pos(self.human.mob_pos())
                self.eq.delete_item()
        elif keys[pygame.K_0] and self.eq.free_slots != set() and self.worn_items.it_on_item():
            self.take_off()            
        elif keys[pygame.K_UP]:
            self.human_attack((0, -move_size))
        elif keys[pygame.K_DOWN]:
            self.human_attack((0,  move_size))
        elif keys[pygame.K_LEFT]:
            self.human_attack((-move_size, 0))
        elif keys[pygame.K_RIGHT]:
            self.human_attack(( move_size, 0))
        elif keys[pygame.K_u] and self.eq.it_on_item():
            self.use_curr_item()
    
    def empty_room(self, pos):
        if pos in self.rooms:
            if self.human.mob_pos() != pos:
                for e in self.mobs:
                    if e.mob_pos() == pos:
                        return False
                return True
        return False
        
    def mob_actions(self):
        for i in range(len(self.mobs)):
            if self.tick % self.mobs[i].speed != 0:
                continue
            distance = dist(self.mobs[i].mob_pos(), self.human.mob_pos())
            if distance <= 1.02 * move_size:
                # attack
                if random_action(self.mobs[i].accuracy):
                    self.human.hurt(max(0, self.mobs[i].attack - self.human.defence), self.tick)
                else:
                    self.human.hurt(0, self.tick)
                # steal item
                if random_action(self.mobs[i].thieving) and len(self.eq.free_slots) != self.eq.slots:
                    while True:
                        el = randint(0, self.eq.slots - 1)
                        if not el in self.eq.free_slots:
                            self.eq.delete_item_from_it(el)
                            self.coms.append((self.tick + coms_time_delay, 
                                              ('  HAHAHAHA! ', yellow, (self.mobs[i].x + 10, self.mobs[i].y + 10))))
                            self.coms.append((self.tick + coms_time_delay, 
                                              ('DID YOU LOSE', yellow, (self.mobs[i].x + 10, self.mobs[i].y + 25))))
                            self.coms.append((self.tick + coms_time_delay, 
                                              (' SOMETHING? ', yellow, (self.mobs[i].x + 10, self.mobs[i].y + 40))))
                            break
                            
            if distance <= mob_move_range:
                # moving
                cands = [(abs(distance - move_size), (0, 0))]
                for e in [(0, move_size), (move_size, 0), (0, -move_size), (-move_size, 0)]:
                    pos_cand = (self.mobs[i].x + e[0], self.mobs[i].y + e[1])
                    if self.empty_room(pos_cand):
                        cands.append((abs(dist(pos_cand, self.human.mob_pos()) - move_size), e))
                self.mobs[i].move(min(cands)[1])                   
            
    def update(self):
        
        # delete dead mobs:
        new_mob_list = []
        for e in self.mobs:
            if e.alive:
                new_mob_list.append(e)
        self.mobs = new_mob_list
        
        # delete old coms:
        new_show_list = []
        for e in self.coms:
            if e[0] > self.tick:
                new_show_list.append(e)
        self.coms = new_show_list
        
        self.mob_actions()
        self.tick += 1
        pygame.time.delay(time_delay)
        self.draw_board()
        if self.human.mob_pos() == self.the_end and len(self.mobs) == 0:
            self.win = True
                
    def run(self):
        self.draw_board()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.human.alive = False
                    break
                if event.type == pygame.KEYDOWN:
                    self.make_action(pygame.key.get_pressed())         
            self.update()
            if not self.human.alive:
                screen.blit(lose_img, (board_size[0] / 2 - 200, board_size[1] / 2 - 100))
                pygame.display.update()
                break
            if self.win:
                screen.blit(win_img,  (board_size[0] / 2 - 200, board_size[1] / 2 - 100))
                pygame.display.update()
                break
            pygame.display.update()
        
        sleep(3)
        pygame.quit()
        sys.exit()
            
