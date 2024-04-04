import pygame
import constants
from character import Character

pygame.init()



screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Danger Dungeon")

# CREATE PLAYER
player = Character(100,100)
# MAIN GAME LOOP
run = True
while run:

    # DRAW PLAYER ON SCRREN
    player.draw(screen)

    # EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # TAKE KEYBOARD PRESSES
            if event.tyoe == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    print("left")
                if event.key == pygame.K_d:
                    print("right")
                if event.key == pygame.K_w:
                    print("up")
                if event.key == pygame.K_s:
                    print("down")
                        
    pygame.display.update()
pygame.quit()