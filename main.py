import pygame
from pygame.display import set_allow_screensaver
from pygame.sprite import GroupSingle
import constants
from character import Character
from weapon import Weapon
# from damageText import DamageText
from items import Item
from world import World

pygame.init()

screen = pygame.display.set_mode(
    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Danger Dungeon")

# MAINTAIN FRAMERATE
clock = pygame.time.Clock()

# DEFINE GAME VARIABLES
level1 = 1



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
healthEmpty = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
healthHalf = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
healthFull = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# COIN IMAGES
coinImages = []
for x in range(4):
  img = scale_image(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
  coinImages.append(img)

red_potion = scale_image(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)

# TILE MAP
tileList = []
for x in range(constants.TILE_TYPES):
  tileImage = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
  tileImage = pygame.transform.scale(tileImage, (constants.TILE_SIZE, constants.TILE_SIZE))
  tileList.append(tileImage)


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

# FUNTION FOR OUTPUTTING TEXT TO THE SCREEN
def drawText(text, font, textColor, x, y):
  img = font.render(text, True, textColor)
  screen.blit(img, (x,y))
  
# FUNCTION FOR DISPLAYING GAME INFO
def draw_info():
  pygame.draw.rect(screen, constants.PANEL, (0,0, constants.SCREEN_WIDTH, 50))
  pygame.draw.line(screen, constants.WHITE, (0,50), (constants.SCREEN_WIDTH, 50))
  healthHalfDrawn = False
  for i in range(5):
    if player.health >= ((i + 1) * 20):
      screen.blit(healthFull, (10 + i * 50, 0))
    elif (player.health % 20 > 0) and healthHalfDrawn == False:
      screen.blit(healthHalf, (10 + i * 50, 0))
      healthHalfDrawn = True
    else:
      screen.blit(healthEmpty, (10 + i * 50, 0))

  # SHOW SCORE
  drawText(f"X{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

# CREATE EMPTY TILE LIST
worldData = []
for row in range(constants.ROWS):
  r = [-1] * constants.COLS
  worldData.append(r)
# LOAD LEVEL DATA AND CREATE WORLD
with open("levels/level1_data.csv", newline="") as csvfile:
  reader = csv.reader(csvfile, delimiter = ",")


world = World()
world.processData(worldData, tileList)


# def drawGrid():
#   for x in range(30):
#     pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
#     pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREEN_WIDTH, x * constants.TILE_SIZE))

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
player = Character(100, 100,70, mob_animations, 0)

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

itemGroup = pygame.sprite.Group()

scoreCoin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coinImages)
itemGroup.add(scoreCoin)

potion = Item(200, 200, 1,[red_potion])
itemGroup.add(potion)
coin = Item(400,400, 0, coinImages)
itemGroup.add(coin)



# MAIN GAME LOOP
run = True
while run:

  # CONTROL FRAME
  clock.tick(constants.FPS)
  # CHANGE BACKGROUND COLOR
  screen.fill(constants.BG)

  # drawGrid()

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
  itemGroup.update(player)


  # DRAW PLAYER ON SCRREN
  world.draw(screen)
  for enemy in enemy_group:
    enemy.draw(screen)
  player.draw(screen)
  bow.draw(screen)
  for arrow in arrow_group:
    arrow.draw(screen)
  damage_text_group.draw(screen)
  # print(enemy.health)
  itemGroup.draw(screen)
  draw_info()
  scoreCoin.draw(screen)
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