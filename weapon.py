import pygame
import math
import constants
import random


class Weapon():
  def __init__(self, image, arrowImage):
    self.original_image = image
    self.angle = 0
    self.arrowImage = arrowImage
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.fired = False
    self.lastShot = pygame.time.get_ticks()
    
  def update(self, player):
    shotCooldown = 300
    arrow = None
    self.rect.center = player.rect.center
    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - self.rect.centerx
    y_dist = -(pos[1] - self.rect.centery)
    self.angle = math.degrees(math.atan2(y_dist, x_dist))
    # GET MOUSE CLICK
    if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.lastShot) >= shotCooldown:
      arrow = Arrow(self.arrowImage, self.rect.centerx, self.rect.centery, self.angle)
      self.fired = True
      self.lastShot = pygame.time.get_ticks()
    if pygame.mouse.get_pressed()[0] == False:
      self.fired = False
    return arrow
    
  def draw(self, surface):
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/ 2)))

class Arrow(pygame.sprite.Sprite):
  def __init__(self, image, x, y, angle):
    pygame.sprite.Sprite.__init__(self)
    self.original_image = image
    self.angle = angle
    self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    # CALCULATE MOVEMENT SPEED BASED ON ANGLE
    self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
    # NEGATIVE BECAUSE PYGAME COORDINANTES FOR Y ARE FLIPPED OR NEGATVE

    self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED) 
    
  def update(self, screenScroll, enemy_group):
    # RESET VARIABLES
    damage = 0
    damagePos = None
    
    # REPOSITION BASED ON SPEED
    self.rect.x += screenScroll[0] + self.dx    
    self.rect.y += screenScroll[1] + self.dy

    # CHECK IF ARROW HAS GONE OFF SCREEN
    if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
      self.kill()
    # CHECL COLLISION OF ARROW AND ENEMY
    for enemy in enemy_group:
      if enemy.rect.colliderect(self.rect) and enemy.alive:
        damage = 10 + random.randint(-5, 5)
        damagePos = enemy.rect
        enemy.health -= damage
        self.kill()
        break
    return damage, damagePos
  

  def draw(self,surface):
    surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/ 2)))