import random
import time
import pickle
from header import *
import menu
import pause
import winlose
from settings import *
from enemies import *


def newGameScreen(level, status = None, pablo = None, hazards = None, windows=None):
    pygame.display.set_caption('ROTTEN TOWER')
    
    # initial variables are set to a default setting or to the paramters I have sent into the function, the latter only happens when pausing and unpausing 
    numberOfLives = 5 if status == None else status[0]
    timeForLevel = level_settings[level -1].time if status == None or len(status) == 1 else status[1]
    numberOfCleans = 0 if status == None or len(status) == 1 else status[2]

    numberOfWindows = level_settings[level -1].windows
    numberOfStains =level_settings[level -1].stains
    numberOfFires =level_settings[level -1].fires
   
    # as stains and fires are removed upon cleaning, when I pause I save what's been cleaned and what has not
    # windows is different as the sprite is changed instead of removed and the position remains the same
    stainsCleanedArray = [] if hazards == None else hazards[0]
    stainRectX = [] if hazards == None else hazards[1]
    stainRectY = [] if hazards == None else hazards[2]
    
    firesCleanedArray = [] if hazards == None else hazards[3]
    firesRectX = [] if hazards == None else hazards[4]
    firesRectY = [] if hazards == None else hazards[5]
    
    windowsDirty = [] if windows == None else windows[0]

    # setting pablo's start position if the game is not paused
    pabloStartX = 670 if pablo == None else pablo[0]
    pabloStartY = PABLO_Y_LIMIT if pablo == None else pablo[1]
    # seagulls and gargoyles start at no speed but it quicly adds speed as it starts moving
    seagullPositionIncrease = 0
    gargoylePositionIncrease = 0
    isGamePaused=False


    # creating two arrays with all the window images in them, one for clean and one for dirty
    for y in range(numberOfWindows):
        towerWindows.append(pygame.image.load(f"windows/window-{y}-clean.png").convert_alpha())
        towerWindowsDirty.append(pygame.image.load(f"windows/window-{y}-dirty.png").convert_alpha())
        windowsDirty.append(True)
   
    # loads the tower image 
    tower = pygame.image.load(f'tower/level-{level}-building.png').convert_alpha()
    towerRect = pygame.Rect(0, 0, SCREEN_WIDTH,SCREEN_HEIGHT)
       
    # to determine how long it's been since the level started
    startTicks=pygame.time.get_ticks() 
    # holds how much time each level has 
    seconds = timeForLevel

    # setting pablo's initial position 
    pabloLocationX = pabloStartX
    pabloLocationY = pabloStartY

    # loading pablo's sprite, creating a pygame rectange so he can be interactable later on
    pablo = pygame.image.load('characters/pablo.png').convert_alpha()
    pabloRect = pygame.Rect(pabloLocationX, pabloLocationY, 28,37)

    # if hazards has not been passed into the parameter, all the stains and fires respectively will be drawn later on (building an array of stains and fires)
    if hazards == None:
        for i in range(numberOfStains):
            stainArray.append(pygame.image.load(f"stains/Stain-{i}.png").convert_alpha())
            stainRectX.append(random.randint(towerStartLocationX,(towerStartLocationX * 2) - 30))
            stainRectY.append(random.randint(towerStartLocationY,pabloStartY))
            stainsCleanedArray.append(True)
    
        for i in range(numberOfFires):
            # I am drawing the fires in specific positions
            # the x-position is either to the left of the tower, the right of the tower or the middle of the tower
            # I am then loading the relevant fire sprite into the fires array 
            xPosition = 390 if i > 3 else 900
            xPosition = xPosition if i < 8 else 630
            firesArray.append(pygame.image.load(f"fires/fire-{i}.png").convert_alpha())
            firesRectX.append(xPosition)
            firesRectY.append(firesYLocations[i])
            firesCleanedArray.append(True)

    # if hazards has not been passed through as a parameter draw all the stains and all the fires 
    # otherwise draw the fires or stains that have not been cleaned yet      
    else:
        for i in range(numberOfStains):          
            stainArray.append(pygame.image.load(f"stains/Stain-{i}.png").convert_alpha()) # 
        for i in range(numberOfFires):          
            firesArray.append(pygame.image.load(f"fires/fire-{i}.png").convert_alpha())


    # start of the main game loop where I am drawing everything to the screen
    run=True
    while run==True:
        screen.fill((0, 0, 0)) # start of each loop, clear the screen, this is so I set up a canvas for everything to be drawn on top of
        screen.blit(tower, tower.get_rect(center = towerRect.center))
        secondsTotal=timeForLevel - (pygame.time.get_ticks()-startTicks)/1000 # calculate how many seconds
        if secondsTotal<1: # if the time is less than 1 second, you have died  
            winlose.successFailGameScreen(False, level, numberOfLives) # show the fail game screen, it shows you the fail one as you have died and false is being sent as the first paramater 


        minutes = int(secondsTotal / 60) % 60
        seconds = secondsTotal % 60
       
        # finding out the percentage of how far into the level you are by dividing numberOfCleans 
        # (incremented anytime you clean anything) by the number of stuff total you need to clean and then timesing that by 100
        # this is to figure out what progress bar sprite to draw  
        font = pygame.font.Font('freesansbold.ttf', 25)
        percentageCleaned = (numberOfCleans == 0 and 0) or numberOfCleans / (numberOfWindows + numberOfStains + numberOfFires) * 100
       
        # code that sets up and displays the timer 
        timerText = font.render(f"{minutes:02}:{round(seconds):02}", True, 'white')
        textRect = timerText.get_rect()
        textRect.center = (700, 40)
        screen.blit(timerText, textRect)

        # sets up and displays the progress bar
        # each block of the progress bar is representative of 10% of your percenteCleaned, this is an example of thinking abstractly 
        status = pygame.image.load('status/progress-bar-{0}.png'.format(round(percentageCleaned / 10))).convert_alpha()
        statusRect = pygame.Rect(950, 0, 179,62)
        screen.blit(status, status.get_rect(center = statusRect.center))

        # sets up and displays the health bar
        lives = pygame.image.load('status/health-{0}.png'.format(numberOfLives)).convert_alpha()
        livesRect = pygame.Rect(200, 0, 179,62)
        screen.blit(lives, lives.get_rect(center = livesRect.center))
        
        # sets up and draws the platforms on the screen by working out the position underneath the window rows on the y-axis
        # to accomplish the look of the platform going off the edge of the tower a bit, I am minusing 15 from the towers starting x-position
        for z in range(numberOfWindowRows):
            towerPlatforms.append(pygame.image.load("tower/platform-{0}.png".format(level)).convert_alpha())
            towerPlatformRect = pygame.Rect(towerStartLocationX - 15, ((z + 1) * (windowPositionOffsetY)) + 50, 478,6)
            screen.blit(towerPlatforms[z], towerPlatforms[z].get_rect(center = towerPlatformRect.center))
       
        # here there are two for loops being set up that first define the x position of the windows
        # these windows are being drawn on the screen using the variable 'numberOfWindowRows' which defines the maximum number of both window rows and columns
        # this variable is then being used to determine the distance between each window horizontally and vertically
        # this is always 90 pixels more horizontally (positionOffsetX) and a 150 more vertically (positionOffsetY)
        for z in range(numberOfWindowRows):
            for x in range(z * (numberOfWindowRows), z * (numberOfWindowRows) + numberOfWindowRows):
                if(x < numberOfWindows):
                    if windowsDirty[x]:
                        windowRect = pygame.Rect(towerStartLocationX + ((x - (z * (numberOfWindowRows))) * windowPositionOffsetX), (z * windowPositionOffsetY) + towerStartLocationY, 70,70)
                        screen.blit(towerWindowsDirty[x], towerWindows[x].get_rect(center = windowRect.center))
                    else:
                        windowRect = pygame.Rect(towerStartLocationX + ((x - (z * (numberOfWindowRows))) * windowPositionOffsetX), (z * windowPositionOffsetY) + towerStartLocationY, 70,70)
                        screen.blit(towerWindows[x], towerWindows[x].get_rect(center = windowRect.center)) 
        

        # obtaining the stain from the array it is held in to draw on the screen  
        for i in range(len(stainsCleanedArray)):
             if stainsCleanedArray[i]:
                 stainRect = pygame.Rect(stainRectX[i],stainRectY[i], 67,72)
                 screen.blit(stainArray[i], stainArray[i].get_rect(center = stainRect.center))

        # obtaining the fires from the array it is held in to draw on the screen
        for i in range(len(firesCleanedArray)):
            if firesCleanedArray[i]:
                firesRect = pygame.Rect(firesRectX[i],firesRectY[i], 67,72)
                screen.blit(firesArray[i], firesArray[i].get_rect(center = firesRect.center))
        
        key=pygame.key.get_pressed()

        # if you press 'a' you're moving pablo to the left
        if key[pygame.K_a] == True and pabloRect.x > towerStartLocationX - 15:
            pabloRect.move_ip(-pabloMoveAmount,0)

        # if you're pressing 'd' you're moving pablo to the right 
        elif key[pygame.K_d] == True and pabloRect.x < (towerStartLocationX * 2) - 15:
            pabloRect.move_ip(pabloMoveAmount,0)
        
        elif key[pygame.K_s] == True and pabloRect.y < PABLO_Y_LIMIT: # if pablo is right at the bottom of the tower sprite do not move him down anymore 
            pabloRect.move_ip(0,pabloMoveAmount)
        
        elif key[pygame.K_w] == True and pabloRect.y > towerStartLocationY: # if pablo is right at the top of the tower sprite do not move up anymore
            pabloRect.move_ip(0,-pabloMoveAmount)

        elif key[pygame.K_ESCAPE] == True: # all the loations of the sprites are saved when you press escape (adds to arrays all the elements in the game)
            enemnySettings = []
            pabloSettings=[]
            statusSettings=[]
            windowSettings=[]
            pabloSettings.append(pabloRect.x)
            pabloSettings.append(pabloRect.y)
            
            enemnySettings.append(stainsCleanedArray)
            enemnySettings.append(stainRectX)
            enemnySettings.append(stainRectY)
            
            enemnySettings.append(firesCleanedArray)
            enemnySettings.append(firesRectX)
            enemnySettings.append(firesRectY)

            statusSettings.append(numberOfLives)
            statusSettings.append(secondsTotal)
            statusSettings.append(numberOfCleans)
            statusSettings.append(level)
            windowSettings.append(windowsDirty)

            # this section saves the above arrays into files using the pickle library (imported at the top)
            with open("saveGameStatus", "wb") as f:
                pickle.dump(statusSettings, f)
            with open("saveGamePablo", "wb") as f:
                pickle.dump(pabloSettings, f)
            with open("saveGameHazards","wb") as f:
                pickle.dump(enemnySettings, f)
            with open("saveGameWindows","wb") as f:
                pickle.dump(windowSettings, f)
            
            # then I go to the pause game screen after having saved all the game's elements 
            pause.pauseGameScreen(level)
              
        screen.blit(pablo, pablo.get_rect(center = pabloRect.center))

        # defining the enemies movement whilst the game is not paused (so enemies do not hit you whilst the game is paused)
        # there position is being increased to give the illusion of movement across the screen
        if(not isGamePaused):
            if(seagullPositionIncrease > SCREEN_WIDTH - 380):
                seagullPositionIncrease = 0
            else:
                seagullPositionIncrease +=5

            if(gargoylePositionIncrease > SCREEN_WIDTH - 380):
                gargoylePositionIncrease = 0
            else:
                gargoylePositionIncrease +=5

        # if the level has seagulls,I am setting up the recatngles of the sprite based on how far they have moved
        # and then draw them to the screen      
        if(level_settings[level -1].seagulls):
            seagullLeftRect = pygame.Rect(200 + seagullPositionIncrease, 100, 48,25)
            seagullRightRect = pygame.Rect((SCREEN_WIDTH - 200) - seagullPositionIncrease, 300, 48,25)
            seagullLeft2Rect = pygame.Rect(200 + seagullPositionIncrease, 500, 48,25)
            seagullRight2Rect = pygame.Rect((SCREEN_WIDTH - 200) - seagullPositionIncrease, 600, 48,25)

            screen.blit(seagullLeft, seagullLeft.get_rect(center = seagullLeftRect.center))
            screen.blit(seagullRight, seagullRight.get_rect(center = seagullRightRect.center))
            screen.blit(seagullLeft2, seagullLeft2.get_rect(center = seagullLeft2Rect.center))
            screen.blit(seagullRight2, seagullRight2.get_rect(center = seagullRight2Rect.center))
        
        # if the level has gargoyles,I am setting up the recatngles of the sprite based on how far they have moved
        # and then draw them to the screen
        if(level_settings[level -1].gargoyles):
            gargoyleLeftRect = pygame.Rect(200 + gargoylePositionIncrease, 200, 48,25)
            gargoyleRightRect = pygame.Rect((SCREEN_WIDTH - 200) - gargoylePositionIncrease, 400, 48,25)
            gargoyleLeft2Rect = pygame.Rect(200 + gargoylePositionIncrease, 530, 48,25)
            gargoyleRight2Rect = pygame.Rect((SCREEN_WIDTH - 200) - gargoylePositionIncrease, 750, 48,25)

            screen.blit(gargoyleLeft, gargoyleLeft.get_rect(center = gargoyleLeftRect.center))
            screen.blit(gargoyleRight, gargoyleRight.get_rect(center = gargoyleRightRect.center))
            screen.blit(gargoyleLeft2, gargoyleLeft2.get_rect(center = gargoyleLeft2Rect.center))
            screen.blit(gargoyleRight2, gargoyleRight2.get_rect(center = gargoyleRight2Rect.center))        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            # here I am detecting if there is a click event that has been detected, determine if the pablo Rect is in the range of the window Rect by using collidepoint
            # if they are not already, update the cleanedArray and the Number of cleans (these determine your level progress) and the window is cleaned
            if event.type == pygame.MOUSEBUTTONDOWN:
                 for z in range(numberOfWindowRows):
                    for x in range(z * (numberOfWindowRows), z * (numberOfWindowRows) + numberOfWindowRows):
                        if(x < numberOfWindows):
                            windowRect = pygame.Rect(towerStartLocationX + ((x - (z * (numberOfWindowRows))) * windowPositionOffsetX), (z * windowPositionOffsetY) + towerStartLocationY, 70,70)
                            if windowRect.collidepoint(pabloRect.x,pabloRect.y) and windowsDirty[x]:
                                windowsDirty[x] = False
                                numberOfCleans+=1
                        
                               
                                screen.blit(towerWindows[x], towerWindows[x].get_rect(center = windowRect.center))
                              
                
                 
                 # here I am checking if there is a click event that has been detected, determine if the pablo Rect is in the range of the stain Rect by using collidepoint
                 # if they are not already, update the cleanedArray and the Number of cleans (these determine your level progress) and the stain is cleaned
                 for s in range(numberOfStains):
                    stainRect = pygame.Rect(stainRectX[s],stainRectY[s], 67,72)
                    
                    if stainRect.collidepoint(pabloRect.x,pabloRect.y) and stainsCleanedArray[s]:
                        stainsCleanedArray[s] = False
                        numberOfCleans+=1

                 # here I am checking if there is a click event that has been detected, determine if the pablo Rect is in the range of the fire Rect by using collidepoint
                 # if they are not already, update the cleanedArray and the Number of cleans (these determine your level progress) and the fire is cleaned 
                 for s in range(numberOfFires):
                    firesRect = pygame.Rect(firesRectX[s],firesRectY[s], 67,72)
                    
                    if firesRect.collidepoint(pabloRect.x,pabloRect.y) and firesCleanedArray[s]:
                        firesCleanedArray[s] = False
                        numberOfCleans+=1
     
        # defining the scenario of enemy/player collisions for all four seagulls             
        if level_settings[level -1].seagulls:
            if(
                pabloRect.collidepoint(seagullLeftRect.x, seagullLeftRect.y) 
                or pabloRect.collidepoint(seagullRightRect.x, seagullRightRect.y)
                or pabloRect.collidepoint(seagullLeft2Rect.x, seagullLeft2Rect.y) 
                or pabloRect.collidepoint(seagullRight2Rect.x, seagullRight2Rect.y)
                ):
                # once the player is hit, the seagulls go back to their start position on the screen and pablo loses a life
                seagullPositionIncrease = 0
                gargoylePositionIncrease = 0
                if(not isGamePaused):
                    numberOfLives-=1
                    isGamePaused=True
                    
                    # moves pablo to the bottom of the screen instantly when he is hit 
                    for i in range (0, 500, 1):          
                        if(pabloRect.y <= pabloStartY):
                            pabloRect.move_ip(0,1)
                    # if you have lost all your lives, go to the fail screen
                    if(numberOfLives == 0):
                        winlose.successFailGameScreen(False, level, numberOfLives)
                    else:
                        isGamePaused=False

        # defining the scenario of enemy/player collisions for all four gargoyles
        if level_settings[level -1].gargoyles:
            if(
                pabloRect.collidepoint(gargoyleLeftRect.x, gargoyleLeftRect.y)
                or pabloRect.collidepoint(gargoyleRightRect.x, gargoyleRightRect.y)
                or pabloRect.collidepoint(gargoyleLeft2Rect.x, gargoyleLeft2Rect.y) 
                or pabloRect.collidepoint(gargoyleRight2Rect.x, gargoyleRight2Rect.y)
            ):
                    # once the player is hit, the gargoyles go back to their start position on the screen and pablo loses two lives
                    seagullPositionIncrease = 0
                    gargoylePositionIncrease = 0
                    if(not isGamePaused):
                            if numberOfLives == 1:
                                numberOfLives-=1
                                isGamePaused=True
                            else:
                                 numberOfLives-=2
                                 isGamePaused=True
                            
                            # moves pablo to the bottom of the screen instantly when he is hit 
                            for i in range (0, 500, 1):          
                                if(pabloRect.y <= pabloStartY):
                                    pabloRect.move_ip(0,1)
                            # if you have lost all your lives, go to the fail screen
                            if(numberOfLives == 0):
                                winlose.successFailGameScreen(False, level, numberOfLives)
                            else:
                                isGamePaused=False
        
        # this describes the scenario of passing the level wherein you have cleaned everything on the tower
        # the game is then saving after you finished the level if you have not completed the game 
        # once the game is complete, your save is deleted 
        if numberOfCleans == numberOfWindows + numberOfStains + numberOfFires:
            if level != numberOflevels:
             enemnySettings = []
             pabloSettings=[]
             statusSettings=[]
             windowSettings=[]
             pabloSettings.append(pabloRect.x)
             pabloSettings.append(pabloRect.y)
                
             enemnySettings.append(stainsCleanedArray)
             enemnySettings.append(stainRectX)
             enemnySettings.append(stainRectY)
                
             enemnySettings.append(firesCleanedArray)
             enemnySettings.append(firesRectX)
             enemnySettings.append(firesRectY)

             statusSettings.append(numberOfLives)
             statusSettings.append(secondsTotal)
             statusSettings.append(numberOfCleans)
             statusSettings.append(level + 1)
             windowSettings.append(windowsDirty)


             with open("saveGameStatus", "wb") as f:
                pickle.dump(statusSettings, f)
             with open("saveGamePablo", "wb") as f:
                pickle.dump(pabloSettings, f)
             with open("saveGameHazards","wb") as f:
                pickle.dump(enemnySettings, f)
             with open("saveGameWindows","wb") as f:
                pickle.dump(windowSettings, f)
            winlose.successFailGameScreen(True, level, numberOfLives)

        pygame.display.update()
