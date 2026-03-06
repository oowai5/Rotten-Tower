from header import *
from controls import newGameControls
# from description import newGameNewspaper
import description

# loading the tutorial screen sprite
def newGameTutorial():
    pygame.display.set_caption('Tutorial')
    background = pygame.image.load("screens/tutorial.png").convert()
    run=True
    
    # drawing the continue button to allow you to progress to next screen
    while run==True:
        mouse = pygame.mouse.get_pos()
        screen.blit(background,(0,0))
        screen.blit(continueSurfaceOff, continueSurfaceOff.get_rect(center = continueButton.center))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continueButton.collidepoint(event.pos):
                    # if you press the continue button, you then go to the controls screen
                    newGameControls()
                if backButton.collidepoint(event.pos):
                    # pressing the back button sends you back to the newspaper screen
                    description.newGameNewspaper()

        # draw the back button
        screen.blit(backSurface, backSurface.get_rect(center = backButton.center))
        exitbuttonHover = backButton.collidepoint(mouse)
        if exitbuttonHover:
            screen.blit(backSurfaceOn, backSurfaceOn.get_rect(center = backButton.center))
       
        # draw the continue button
        continuebuttonHover = continueButton.collidepoint(mouse)
        if continuebuttonHover:
            screen.blit(continueSurfaceOn, continueSurfaceOn.get_rect(center = continueButton.center))
          

        pygame.display.update()