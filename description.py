from header import *
from tutorial import newGameTutorial
import menu

# loading the newspaper screen sprite
def newGameNewspaper():
     pygame.display.set_caption('About')
     background = pygame.image.load("screens/newspaper-screen.png").convert()
     run=True

     # drawing the continue button to allow you to progress to next screen 
     while run==True:
        mouse = pygame.mouse.get_pos()
        screen.blit(background,(0,0))
        screen.blit(continueSurfaceOff, continueSurfaceOff.get_rect(center = continueButton.center))
        
        for event in pygame.event.get():
            # if the user event is clicking on the window cross button, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if continueButton.collidepoint(event.pos):
                    # if you press the continue button, you then go to the tutorial screen
                    newGameTutorial()
                if backButton.collidepoint(event.pos):
                    # if you press the back button, you go back to the main menu
                    menu.mainMenu()
                    
       
        # draw the back button (sends you back to prior screen)
        screen.blit(backSurface, backSurface.get_rect(center = backButton.center))
        exitbuttonHover = backButton.collidepoint(mouse)
        if exitbuttonHover:
            screen.blit(backSurfaceOn, backSurfaceOn.get_rect(center = backButton.center))

        # draw the continue button (sends you to next screen)
        continuebuttonHover = continueButton.collidepoint(mouse)
        if continuebuttonHover:
             screen.blit(continueSurfaceOn, continueSurfaceOn.get_rect(center = continueButton.center))
    

        pygame.display.update()