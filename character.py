import pygame
import constants
import math

class Character():
    def __init__(self, x, y, animation_list):
    #     self.char_type = char_type
    #     self.boss = boss
    #     self.score = 0
        self.flip = False
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:run
        self.update_time = pygame.time.get_ticks()
        self.running = False
    #     self.health = health
    #     self.alive = True
    #     self.hit = False
    #     self.last_hit = pygame.time.get_ticks()
    #     self.last_attack = pygame.time.get_ticks()
    #     self.stunned = False

        self.image = animation_list[self.action][self.frame_index]
        # self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect = pygame.Rect(0, 0, 40, 40)
        
        self.rect.center = (x, y)
       
    def move(self, dx, dy):
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
            
            
        # FLIPPING CHARACTER IMAGE FOR TURNING
        if dx < 0:
            self.flip = True
        if dy < 0:
            self.flip = False
            
        # CONTROL DIAGONAL SPEED
        if dx != 0 and dy != 0 :
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
            
        
        # ADJUST PLAYER FOR MOVEMENT
        self.rect.x += dx
        self.rect.y += dy         
        
    def update(self):
        # CHECK WHAT ACTION THE PLAYER IS PERFORMING
        if self.running == True:
            self.update_action(1) # RUN
        else:
            self.update_action(0) # IDLE
            
        animation_cooldown = 70
        #HANDLE ANIMATION SPEED
        self.image = self.animation_list[self.action][self.frame_index]
        # CHECK IF ENOUGH TIME HAS PASSED SINCE THE LAST UPDATE
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()      
        # CHECK IF THE ANIMATION HAS FINISHED
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            
    def update_action(self, new_action):
        # CHECK IF THE NEW ACTION IS DIFFERENT          
        if new_action != self.action:
            self.action = new_action
            # UPDATE THE ANIMATION SETTINGS
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()    
        
            
        
    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface,constants.RED, self.rect, 1)