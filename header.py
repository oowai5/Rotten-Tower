import pygame
import os

# set up the game screen and the limit to pablo's y-axis movement (so he does not go off the screen)
SCREEN_WIDTH=1366
SCREEN_HEIGHT=784
PABLO_Y_LIMIT=740
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# loading the sprites for the back button, try again button and continue button
# setting up a rectangle for these three sprites so they are all interactable
backSurface = pygame.image.load('buttons/exit-on.png').convert_alpha()
backSurfaceOn = pygame.image.load('buttons/exit-off.png').convert_alpha()
tryAgainSurfaceOn = pygame.image.load('buttons/try-again-off.png').convert_alpha()
tryAgainSurfaceOff = pygame.image.load('buttons/try-again-on.png').convert_alpha()
continueSurfaceOff = pygame.image.load('buttons/continue-off.png').convert_alpha()
continueSurfaceOn = pygame.image.load('buttons/continue-on.png').convert_alpha()
continueButton = pygame.Rect(990,670,201,91)
backButton = pygame.Rect(210,-30,114,124)
tryAgainButton = pygame.Rect((SCREEN_WIDTH / 2) - 154, (SCREEN_HEIGHT / 2) - 55,308,110)

# defining the number of levels 
numberOflevels = 3