from header import *
import os
import pickle
from description import newGameNewspaper
from gameplay import newGameScreen
import levelbrief

def mainMenu():
    # the main menu screen
    # set caption for window 
    pygame.display.set_caption('Main Menu')
    background = pygame.image.load("screens/startup_screen.png").convert()

    
    # set the loop variable to true, this could be called anything like running, start etc I called it run
    run=True
    
    # start the game loop
    while run==True:
        screen.blit(background,(0,0))

        # get the mouse position and if it is currently being cliked
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        # this would ideally be a separate method as I am repeating most of the code for each menu button

        # create two images one for not hovering and one for hovering
        newGameImage = pygame.image.load('buttons/newGameCrop1.png').convert_alpha()
        newGameImageOn = pygame.image.load('buttons/newGameCrop2.png').convert_alpha()
        
        # create a surface (Rect) to put on above loaded images
        newGameRect = pygame.Rect(600, 214, 167, 30)

        # check if the mouse position from above is colliding with the surface
        newGameOnButton = newGameRect.collidepoint(mouse)

        # draw the relevant image I loaded above if the mouse position is on the surface or not on it. Hover image or non hovered image
        if newGameOnButton:
            screen.blit(newGameImageOn, newGameImageOn.get_rect(center = newGameRect.center))
        else:
            screen.blit(newGameImage, newGameImage.get_rect(center = newGameRect.center))

        # setting up continue game button
        continueGameImage = pygame.image.load('buttons/continueGameCrop1.png').convert_alpha()
        continueGameImageOn = pygame.image.load('buttons/continueGameCrop2.png').convert_alpha()
        continueGameRect = pygame.Rect(600, 415, 167,30)
        continueGameOnButton = continueGameRect.collidepoint(mouse)

        if continueGameOnButton:
            screen.blit(continueGameImageOn, continueGameImageOn.get_rect(center = continueGameRect.center))
        else:
            screen.blit(continueGameImage, continueGameImage.get_rect(center = continueGameRect.center))

       
        # setting up quit game button
        quitGameImage = pygame.image.load('buttons/quitGameCrop1.png').convert_alpha()
        quitGameImageOn = pygame.image.load('buttons/quitGameCrop2.png').convert_alpha()
        quitGameRect = pygame.Rect(600, 644, 167,30)
        quitGameOnButton = quitGameRect.collidepoint(mouse)

        if quitGameOnButton:
            screen.blit(quitGameImageOn, quitGameImageOn.get_rect(center = quitGameRect.center))
        else:
            screen.blit(quitGameImage, quitGameImage.get_rect(center = quitGameRect.center))


        # handling the menu buttons clicks/events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.quit()
                run = False

            # go to the relevant method (game screen) depending on which button has been pressed using the click ad OnButton variables
            # check to see if there are saved files and delete them if there are as the game always delete old files when I start a new game
            if newGameOnButton:  
                if click[0] == 1:
                    if os.path.exists("saveGameStatus"):
                        os.remove("saveGameStatus")
                    if os.path.exists("saveGamePablo"):
                        os.remove("saveGamePablo")
                    if os.path.exists("saveGameHazards"):
                        os.remove("saveGameHazards")
                    if os.path.exists("saveGameWindows"):
                        os.remove("saveGameWindows")
                    newGameNewspaper()
                    
            # same as above but for continue button, this will only work if saves exist and if so they are laoded and you are sent to the level brief of the level you are on
            elif continueGameOnButton:  
                if click[0] == 1:
                     if os.path.exists("saveGameStatus"):
                        with open("saveGameStatus", "rb") as f:
                            status = pickle.load(f)
                        with open("saveGamePablo", "rb") as f:
                            pablo = pickle.load(f)
                        with open("saveGameHazards", "rb") as f:
                            hazards = pickle.load(f)
                        with open("saveGameWindows", "rb") as f:
                            windows = pickle.load(f)

                        run=False
                        levelbrief.newGameBrief(status[3],5)
                    
            elif quitGameOnButton:
                if click[0] == 1:
                     pygame.quit()
                     run = False
            
        pygame.display.update()
