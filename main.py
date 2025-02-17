import pygame
# from pygame import mixer      
import constants
from character import Character
from weapon import Weapon


# MIXER & PYGAME INITIALIZED
# mixer.init()
pygame.init()

# FIX  MAIN GAME SCREEN AND DISPLAY NAME
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("dangerDungeon")

# FRAMERATE CLOCK
clock = pygame.time.Clock()

# DEFINE PLAYER MOVEMENT
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# DEFINE FONT
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

player_img = pygame.image.load("assets/images/characters/elf/idle/0.png").convert_alpha()
# SCALE IMAGE
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w  * scale, h * scale))

# LOAD BOW & ARROW IMAGES / AND SCALE
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)


# BODY MOVEMENT ANIMATION
animation_types = ["idle", "run"]

# LOAD CHARACTER IMAGES
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]

# LOAD MOB
for mob in mob_types: 
      
    # LOAD PLAYER
    animation_list = []
    
    for animation in animation_types:
        # RESET TEMPORARY LIST
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)
    
    
    # ANIMATION LIST (TESTING)
    # print(animation_list)

# DAMAGE TEXT CLASS
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    
# CREATE PLAYER
player = Character(100, 100, 100, mob_animations, 0)

# CREATE ENEMY
enemy = Character(200, 300, 100, mob_animations, 1)

# CREATE PLAYER WEAPON - THIS IS THE MAIN PASS IN POINT FOR THE ARROW TO WEAPON CLASS
bow = Weapon(bow_image, arrow_image)

# DAMAGE TEXT SPRITE GROUP
damage_text_group = pygame.sprite.Group()

# TEMPORARY DAMAGE TEXT
damage_text = DamageText(300, 400, 15, constants.RED)
damage_text_group.add(damage_text)

# CREATE SPRITE GROUPS
arrow_group = pygame.sprite.Group()



# CREATE EMPTY ENEMY LIST
enemy_list = []
enemy_list.append(enemy)

# MAIN GAME LOOP        
run = True
while run:
    
    # CONTROL FRAME RATE
    clock.tick(constants.FPS)
    
    # CLEAR SCREEN
    screen.fill(constants.BG)
    
    
    # SET STARTING POSITION
    dx = 0
    dy = 0
    
    # HANDLE MOVEMENT
    if moving_right == True:
        dx = constants.SPEED
    if moving_left == True:
        dx = -constants.SPEED
    if moving_up == True:
        dy = -constants.SPEED
    if moving_down == True:
        dy = constants.SPEED
        
    # DISPLAY LOCATION
    # print(str(dx) + "," + str(dy))
    
    # MOVE PLAYER
    player.move(dx, dy)
    
    # LOOP THROUGH ENEMY LOOP
    for enemy in enemy_list:
        enemy.update()
        
    # UPDATE PLAYER
    player.update()
    arrow = bow.update(player)
    # CHECK IF ARROWS EXIST IN ARROW GROUP
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        arrow.update(enemy_list) 
    damage_text_group.update()   
    # print(arrow_group)
    
    # LOOP THROUGH ENEMY LOOP
    for enemy in enemy_list:
        enemy.draw(screen)
        
    # DRAW PLAYER & WEAPON ON SCREEN
    player.draw(screen)
    bow.draw(screen)
    # ACCESS ARROW GROUP
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)   
    
    
    print(enemy.health)
    
    
    
    
    # EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            

        # KEY PRESSED
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True 
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True 
                
         # KEY RELEASED
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