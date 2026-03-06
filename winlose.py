from header import *
import os
import levelbrief
import description
import gameplay

# this method is called from gameplay and the parameters it takes are whether you died or not, the level you are on and the number of lives you have
def successFailGameScreen(isSuccessful, level, numberOfLives):
    screen.fill((255, 255, 255))
    gameComplete=False
    pygame.mouse.set_visible(True)
    continueButtonNextLevelRect = pygame.Rect((SCREEN_WIDTH / 2) - 100,(SCREEN_HEIGHT /2) - 45,201,91)
    
    if isSuccessful:
        gameComplete = level == numberOflevels  # is the level you are on the same as the total number of levels in the game 
        pygame.display.set_caption('Success!')
    else:
        pygame.display.set_caption('Failed!')
    
    # start loop
    run=True
    while run==True:
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()
        # determine whether to show the success screen, the fail screen or the game completion screen
        if isSuccessful:  
            if gameComplete: 
                nextScreen = pygame.image.load('screens/win-screen.png').convert_alpha()
            else:
                nextScreen = pygame.image.load('screens/success-game-screen.png').convert_alpha()
            
        else:
            nextScreen = pygame.image.load('screens/fail-game-screen.png').convert_alpha()
            
            
        successFailedRectRect = pygame.Rect(0, 0, SCREEN_WIDTH,SCREEN_HEIGHT)
        screen.blit(nextScreen, nextScreen.get_rect(center = successFailedRectRect.center)) 

        # if you finish the game than delete all the save game files as you have completed the game 
        if gameComplete:
            if os.path.exists("saveGameStatus"):
                os.remove("saveGameStatus")
            if os.path.exists("saveGamePablo"):
                os.remove("saveGamePablo")
            if os.path.exists("saveGameHazards"):
                os.remove("saveGameHazards")
            if os.path.exists("saveGameWindows"):
                os.remove("saveGameWindows")

        # if you passed a level, the quit game and continue game buttons appear on the screen
        # if you failed a level, the quit game and try again buttons appear on the screen
        if(not gameComplete):
            if isSuccessful:
                screen.blit(continueSurfaceOff, continueSurfaceOff.get_rect(center = continueButtonNextLevelRect.center))
                tryAgainButtonHover = tryAgainButton.collidepoint(mouse)
                if tryAgainButtonHover:
                    screen.blit(continueSurfaceOn, continueSurfaceOn.get_rect(center = continueButtonNextLevelRect.center))

            else:
                screen.blit(tryAgainSurfaceOff, tryAgainSurfaceOff.get_rect(center = tryAgainButton.center))
                tryAgainButtonHover = tryAgainButton.collidepoint(mouse)
                if tryAgainButtonHover:
                    screen.blit(tryAgainSurfaceOn, tryAgainSurfaceOff.get_rect(center = tryAgainButton.center))


        quitGameImage = pygame.image.load('buttons/quitGameForPause(clicked).png').convert_alpha()
        quitGameImageOn = pygame.image.load('buttons/quitGameForPause(unclicked).png').convert_alpha()
        quitGameRect = pygame.Rect(580, 470, 201,91)
        quitGameOnButton = quitGameRect.collidepoint(mouse)

        if quitGameOnButton:
            screen.blit(quitGameImageOn, quitGameImageOn.get_rect(center = quitGameRect.center))
        else:
            screen.blit(quitGameImage, quitGameImage.get_rect(center = quitGameRect.center))

        # the click event handler 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tryAgainButton.collidepoint(event.pos):
                    run=False
                    if not isSuccessful:                        
                        levelbrief.newGameBrief(level, 5)
                    else:
                        level +=1
                        levelbrief.newGameBrief(level, 5)

                elif quitGameOnButton:
                   pygame.quit()
                   run = False
                
                
        pygame.display.update()