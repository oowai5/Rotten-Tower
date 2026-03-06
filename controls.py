from header import * 
from levelbrief import newGameBrief
import tutorial

# loading the controls screen sprite
def newGameControls():
    pygame.display.set_caption('Controls')
    background = pygame.image.load("screens/controls.png").convert()
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
                    run=False
                    # this is needed to tell the level brief file which level and how many lives you have 
                    # (this will always start with five lives on a new level)
                    newGameBrief(1, 5)
                if backButton.collidepoint(event.pos):
                    # pressing the back button sends you back to the tutorial screen
                    tutorial.newGameTutorial()


        screen.blit(backSurface, backSurface.get_rect(center = backButton.center))
        exitButtonHover = backButton.collidepoint(mouse)
        if exitButtonHover:
            screen.blit(backSurfaceOn, backSurfaceOn.get_rect(center = backButton.center))
       
        # if the mouse is hovering over the continue button, it sets that as  
        continuebuttonHover = continueButton.collidepoint(mouse)
        if continuebuttonHover:
            screen.blit(continueSurfaceOn, continueSurfaceOn.get_rect(center = continueButton.center))
           
                

        pygame.display.update()