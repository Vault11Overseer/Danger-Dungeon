import pygame
import constants
import math

class Character():
    def __init__(self, x, y, animation_list):
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0#0:idle, 1:run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned = False

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)
       
    def move(self, dx, dy):
        # FLIPPING CHARACTER IMAGE FOR TURNING
        if dx < 0:
            self.flip = True
        if dy < 0:
            self.flip = False
            
        # CONTORL DIAGONAL SPEED
        if dx != 0 and dy != 0 :
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
            
        
        # ADJUST PLAYER FOR MOVEMENT
        self.rect.x += dx
        self.rect.y += dy         
        
    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface,constants.RED, self.rect, 1)