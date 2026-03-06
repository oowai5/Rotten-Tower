
# import python libraries, start pygame, set relevant directory 
import pygame
import os
from menu import mainMenu
import settings
pygame.init()
os.chdir(settings.systemPath)

# start point calling first method
mainMenu()