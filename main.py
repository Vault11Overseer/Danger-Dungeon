import pygame
# from pygame import mixer      
import constants
from character import Character
# MIXER & PYGAME INITIALIZED
# mixer.init()
pygame.init()

# FIX  MAIN GAME SCREEN AND DISPLAY NAME
screen = pygame.display.set_mode(
    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("dangerDungeon")

# CREATE PLAYER
player = Character(100, 100)


# MAIN GAME LOOP        
run = True
while run:
    
    
    # DRAW PLAYER ON SCREEN
    player.draw(screen)
    
    
    # EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            

        # TAKE KEYBOARD PRESSES
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("left")
            if event.key == pygame.K_d:
                print("right")    
            if event.key == pygame.K_d:
                print("up") 
            if event.key == pygame.K_d:
                print("left") 
    
    pygame.display.update()
            
pygame.quit()