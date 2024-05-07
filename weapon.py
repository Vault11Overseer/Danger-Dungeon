import pygame
import math

class Weapon():
  def __init__(self, image, arrowImage):
    self.original_image = image
    self.angle = 0
    self.arrowImage = arrowImage
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()

  def update(self, player):
    arrow = None
    self.rect.center = player.rect.center
    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - self.rect.centerx
    y_dist = -(pos[1] - self.rect.centery)
    self.angle = math.degrees(math.atan2(y_dist, x_dist))
    # GET MOUSE CLICK
    if pygame.mouse.get_pressed()[0]:
      arrow = Arrow(self.arrowImage, self.rect.centerx, self.rect.centery, self.angle)
      
    return arrow
    
  def draw(self, surface):
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/ 2)))

class Arrow(pygame.sprite.Sprite):
  def __init__(self, image, x, y, angle):
    pygame.sprite.Sprite.__init__(self)
    self.original_image = image
    self.angle = angle
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    
  def draw(self,surface):
    