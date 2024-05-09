# DAMAGE TEXT CLASS
class DamageText(pygame.sprite.Sprite):
  def __init__(self, x, y, damage, color):
    pygame.sprite.Sprite.__init__(self)
    self.image = font.render(damage, True, color)
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    self.counter = 0

  def update(self):
    # MOVE DAMAGE TEXT UP
    self.rect.y -= 1
    # DELETE THE COUNTER AFTER A FEW SECONDS
    self.counter += 1
    if self.counter >30:
      self.kill()