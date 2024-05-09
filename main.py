import pygame
from pygame.sprite import GroupSingle
import constants
from character import Character
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode(
    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Danger Dungeon")

# MAINTAIN FRAMERATE
clock = pygame.time.Clock()

# DEFINE PLAYER MOVEMENT
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# DEFINE FONT
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# HELPER FUNCTION TO SCALE IMAGE
def scale_image(image, scale):
  w = image.get_width()
  h = image.get_height()
  return pygame.transform.scale(image, (w * scale, h * scale))

# LOAD WEAPON IMAGES
bowImage = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrowImage = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)

# LOAD CHARACTER IMAGES
mob_animations = []
mob_types = ["elf", "imp", "goblin", "muddy", "tiny_zombie", "big_demon"]
for mob in mob_types:
  
  # LIST OF IMAGES
  animation_list = []
  animation_types = ["idle", "run"]
  
  for animation in animation_types:
    # RESET TEMPORARY LIST OF IMAGES
    temp_list = []
    
    for i in range(4):
      img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha() 
      img = scale_image(img, constants.SCALE)
      temp_list.append(img)
    animation_list.append(temp_list)
  mob_animations.append(animation_list)

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

# CREATE PLAYER
player = Character(100, 100,100, mob_animations, 0)

# CREATE ENEMY
enemy = Character(200,300,100, mob_animations, 1)

# CREATE PLAYERS Weapon
bow = Weapon(bowImage, arrowImage)



# CREATE ENEMY GROUPS
enemy_group = []
enemy_group.append(enemy)
# CREATE DAMAGE TEXT
damage_text_group = pygame.sprite.Group()
# CREATE SPRITE GROUPS
arrow_group = pygame.sprite.Group()



# MAIN GAME LOOP
run = True
while run:

  # CONTROL FRAME
  clock.tick(constants.FPS)
  # CHANGE BACKGROUND COLOR
  screen.fill(constants.BG)

  # CALCULATE PLAYER MOVEWMENT
  dx = 0
  dy = 0
  if moving_right == True:
    dx = constants.SPEED
  if moving_left == True:
    dx = -constants.SPEED
  if moving_up == True:
    dy = -constants.SPEED
  if moving_down == True:
    dy = constants.SPEED 

  
  # UPDATE PLAYER POSITION
  player.move(dx, dy)

  # UPDATE player
  for enemy in enemy_group:
    enemy.update()
  player.update()
  arrow = bow.update(player)
  if arrow:
    arrow_group.add(arrow)
  for arrow in arrow_group:
    damage, damagePos = arrow.update(enemy_group)
    if damage:
      damageText = DamageText(damagePos.centerx, damagePos.centery, str(damage), constants.RED)
      damage_text_group.add(damageText)
  damage_text_group.update()
  


  # DRAW PLAYER ON SCRREN
  for enemy in enemy_group:
    enemy.draw(screen)
  player.draw(screen)
  bow.draw(screen)
  for arrow in arrow_group:
    arrow.draw(screen)
  damage_text_group.draw(screen)


  print(enemy.health)
  # EVENT HANDLER
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    # TAKE KEYBOARD PRESSES
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        moving_left = True
      if event.key == pygame.K_d:
        moving_right = True
      if event.key == pygame.K_w:
        moving_up = True
      if event.key == pygame.K_s:
        moving_down = True
    # TAKE KEYBOARD RELEASES
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        moving_left = False
      if event.key == pygame.K_d:
        moving_right = False
      if event.key == pygame.K_w:
        moving_up = False
      if event.key == pygame.K_s:
        moving_down = False
    

  pygame.display.update()
pygame.quit()