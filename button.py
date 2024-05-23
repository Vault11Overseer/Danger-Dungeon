import pygame
# BUTTON CLASS
class Button():
  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
  # DRAW CLASS
  def draw(self, surface):
    action = False

    # GET MOUSE POSITION 
    pos = pygame.mouse.get_pos()

    # CHECK FOR MOUSE OVER AND CLICK CONDITIONS
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0]:
        action = True
    # BLIT THE SURFACE
    surface.blit(self.image, self.rect)
    
    return action