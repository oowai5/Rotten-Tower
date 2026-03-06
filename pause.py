from header import *
import pickle
import gameplay
  

def pauseGameScreen(level):
    # filling the screen with a solid colour, gives the game a blank canvas by drawing over everything on the previous screen 
    screen.fill((255, 255, 255))
    run=True
    while run==True:
        screen.fill((255, 255, 255))
        mouse = pygame.mouse.get_pos()
        pauseScreen = pygame.image.load('screens/pause.png').convert_alpha()
        pauseScreenRect = pygame.Rect(0, 0, SCREEN_WIDTH,SCREEN_HEIGHT)
        screen.blit(pauseScreen, pauseScreen.get_rect(center = pauseScreenRect.center)) 
        continueButtonPauseRect = pygame.Rect((SCREEN_WIDTH / 2) - 100,(SCREEN_HEIGHT /2) - 45,201,91)
        screen.blit(continueSurfaceOff, continueSurfaceOff.get_rect(center = continueButtonPauseRect.center))

        quitGameImage = pygame.image.load('buttons/quitGameForPause(clicked).png').convert_alpha()
        quitGameImageOn = pygame.image.load('buttons/quitGameForPause(unclicked).png').convert_alpha()
        quitGameRect = pygame.Rect(580, 470, 201,91)
        quitGameOnButton = quitGameRect.collidepoint(mouse)

        if quitGameOnButton:
            screen.blit(quitGameImageOn, quitGameImageOn.get_rect(center = quitGameRect.center))
        else:
            screen.blit(quitGameImage, quitGameImage.get_rect(center = quitGameRect.center))

        continueButtonHover = continueButtonPauseRect.collidepoint(mouse)
        if continueButtonHover:
            screen.blit(continueSurfaceOn, continueSurfaceOff.get_rect(center = continueButtonPauseRect.center))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            # before pressing continue I load the saved status data so this can be passed to gameplay   
            if event.type == pygame.MOUSEBUTTONDOWN:
               with open("saveGameStatus", "rb") as f:
                   status = pickle.load(f)
               with open("saveGamePablo", "rb") as f:
                   pablo = pickle.load(f)
               with open("saveGameHazards", "rb") as f:
                   hazards = pickle.load(f)
               with open("saveGameWindows", "rb") as f:
                   windows = pickle.load(f)
               
               # after I press continue, I remove the save files
               if(continueButtonHover):
                     if os.path.exists("saveGameStatus"):
                        os.remove("saveGameStatus")
                     if os.path.exists("saveGamePablo"):
                        os.remove("saveGamePablo")
                     if os.path.exists("saveGameHazards"):
                        os.remove("saveGameHazards")
                     if os.path.exists("saveGameWindows"):
                        os.remove("saveGameWindows")
                     gameplay.newGameScreen(level, status, pablo, hazards, windows)
                     
               elif quitGameOnButton:
                   pygame.quit()
                   run = False
                   
        pygame.display.update()