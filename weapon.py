import pygame
import math
import constants
import random


class Weapon():
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        # BOW IMAGE
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # ARROW IMAGE
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        # TRIGGER FOR ARROWS
        self.fired = False
        # FIRE COOLDOWN
        self.last_shot = pygame.time.get_ticks()
        
    def update(self, player):
        # FIRE COOLDOWN
        # shot_cooldown = 300
        
        # INITIALIZE ARROW
        arrow = None
        # SET CENTER OF PLAYER
        self.rect.center = player.rect.center
    
        # UPDATE BOW BASED ON MOUSE POSITION
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery) # PYGAME Y COORDINATES INCREASE DOWN SCREEN
        # SET THE ANGLE BASED ON MOUSE POSITION
        self.angle = math.degrees(math.atan2(y_dist, x_dist))        
    
        # GET MOUSE CLICK TOO SHOOT INITIALIZED ARROW THROUGH WEAPON CLASS
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= constants.SHOT_COOLDOWN:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        # RESET FIRED ARROW
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
            

        # RETURN ARROW SO IT CAN BE USED IN THE MAIN FILE
        return arrow
    
            
            
    def draw(self, surface):
        # BEFORE DRAWING IMAGE SET ITS ANGLE BASED ON THE MOUSE POSITION
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # OFFSET BOW CENTER TO EDGE OF RECTANGLE AND DRAW BOW
        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)) )
        
# ARROW CLASS    
class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        # ORIENTATE ARROW
        self.image = pygame.transform.rotate(self.original_image, self.angle -90)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        # CALCULATE HORIZONTAL AND VERTICAL SPEEDS BASED ON THE ANGLE
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = math.sin(math.radians(self.angle)) * constants.ARROW_SPEED
        
        
    def update(self, enemy_list):
        # REPOSITION ARROW BASED ON SPEED
        self.rect.x += self.dx
        self.rect.y += self.dy     
        # CHECK IF ARROW HAS GONE OFF SCREEN
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()
        # CHECK COLLISION BETWEEN ARROW AND ENEMIES
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)
                enemy.health -= damage
                self.kill()
                break
             
        
    def draw(self, surface):
        # OFFSET ARROWS TO MATCH BOW
        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)) )
        