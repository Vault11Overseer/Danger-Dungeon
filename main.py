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

# CREATE PLAYER
player = Character(100, 100, mob_animations, 0)

# CREATE PLAYERS Weapon
bow = Weapon(bowImage, arrowImage)

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
  player.update()
  arrow = bow.update(player)
  if arrow:
    arrow_group.add(arrow)

  print(arrow_group)
  arrow_group.draw(screen)

  # DRAW PLAYER ON SCRREN
  player.draw(screen)
  bow.draw(screen)

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