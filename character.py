import pygame
import constants
import math

class Character():
    def __init__(self, x, y, mob_animations, charType):
        self.flip = False
        self.charType = charType
        self.animation_list = mob_animations[charType]
        self.frameIndex = 0
        self.running = False
        self.action = 0 # 0: idle, 1: run
        self.updateTime = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frameIndex]
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)

    def move(self, dx, dy):
      self.running = False

      if dx != 0 or dy != 0:
        self.running = True
      if dx < 0:
        self.flip = True
      if dx > 0:
        self.flip = False

      # CONTROL DIAGONAL SPEED
      if dx != 0 and dy != 0:
        dx = dx * (math.sqrt(2)/2)
        dy = dy * (math.sqrt(2)/2)

      
      self.rect.x += dx
      self.rect.y += dy


    def update(self):
      # CHECK WHAT ACTION THE PLAYER IS PERFORMING
      if self.running == True:
        self.update_action(1)
      else:
        self.update_action(0)

      
      animationCooldown = 70
      # HANDLE ANIMATION
      # HANDLE IMAGE
      self.image = self.animation_list[self.action][self.frameIndex]
      # CHECK IF ENOUGH TIME HAS PASSED BEFORE UPDATING
      if pygame.time.get_ticks() - self.updateTime > animationCooldown:
        self.frameIndex += 1
        self.updateTime = pygame.time.get_ticks()
      # CHECK IF ANIMATION HAS FINISHED
      if self.frameIndex >= len(self.animation_list[self.action]):
        self.frameIndex = 0

    def update_action(self, new_action):
      # CHECK IF NEW ACTION IS DIFFERENT FROM THE PREVIOUS ACTION
      if new_action != self.action:
        self.action = new_action
        # UPDATE THE ANIMATION TIME
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
      

    def draw(self,  surface):
      flipped_image = pygame.transform.flip(self.image, self.flip, False)
      if self.charType == 0:
        surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
      else:
        surface.blit(flipped_image, self.rect)
      pygame.draw.rect(surface, constants.RED, self.rect, 1)