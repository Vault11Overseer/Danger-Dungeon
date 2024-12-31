import pygame
# from pygame import mixer      
import constants
from character import Character



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


# SCALE IMAGE
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w  * scale, h * scale))

# BODY MOVEMENT ANIMATION
animation_list = []

# LOAD PLAYER
for i in range(4):
    img = pygame.image.load(f"assets/images/characters/elf/idle/{i}.png").convert_alpha()
    img = scale_img(img, constants.SCALE)
    animation_list.append(img)
# CREATE PLAYER
player = Character(100, 100, animation_list)


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
     
    # DRAW PLAYER ON SCREEN
    player.draw(screen)
    
    
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