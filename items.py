import pygame

class Item(pygame.sprite.Sprite):
  def __init__(self, x, y, itemType, animationList, dummyCoin = False):
    pygame.sprite.Sprite.__init__(self)
    self.itemType = itemType
    self.animationList = animationList
    self.frameIndex = 0
    self.updateTime = pygame.time.get_ticks()
    self.image = self.animationList[self.frameIndex]
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    self.dummyCoin = dummyCoin

  def update(self, screenScroll, player):
    # DOESN'T APPLY TO THE DUMMY COIN
    if not self.dummyCoin:
      # REPOSITION BASED ON SCREEN SCROLL
      self.rect.x += screenScroll[0]
      self.rect.y += screenScroll[1]

    if self.rect.colliderect(player.rect):
      # COIN COLLECTED
      if self.itemType == 0:
        player.score += 1
      elif self.itemType == 1:
        player.health += 10
        if player.health > 100:
          player.health = 100
      self.kill()
      
    animationCooldown = 150
    self.image = self.animationList[self.frameIndex]
    
    if pygame.time.get_ticks() - self.updateTime > animationCooldown:
      self.frameIndex += 1
      self.updateTime = pygame.time.get_ticks()
    if self.frameIndex >= len(self.animationList):
      self.frameIndex = 0


  def draw(self, surface):
    surface.blit(self.image, self.rect)