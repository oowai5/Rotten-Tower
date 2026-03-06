from header import *
import gameplay

def newGameBrief(level, numberOfLives):
    pygame.display.set_caption('Level {0}'.format(level))
    
    background = pygame.image.load("screens/level-{0}-brief.png".format(level)).convert()
    
    run=True
    
    while run==True:
        # making an array with the number of lives you have and then sending it as the status paramater for new game screen 
        statusSettings = [];
        statusSettings.append(numberOfLives)
        mouse = pygame.mouse.get_pos()
        screen.blit(background,(0,0))
        screen.blit(continueSurfaceOff, continueSurfaceOff.get_rect(center = continueButton.center))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continueButton.collidepoint(event.pos):
                    run=False
                    gameplay.newGameScreen(level, statusSettings)
       
        # draw the continue button
        continuebuttonHover = continueButton.collidepoint(mouse)
        if continuebuttonHover:
            screen.blit(continueSurfaceOn, continueSurfaceOn.get_rect(center = continueButton.center))
                

        pygame.display.update()