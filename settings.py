from collections import namedtuple

systemPath = ('C:\\Users\\DELL TOWER 5810\\Documents\\OLD SCHOOL STUFF\\Python\\final-updated')
level_settings = []

# using the data structure names tuple (collection) to hold level information which I then store in an array as it is easier to reference within gameplay
level1 = namedtuple('literal', 'stains seagulls windows gargoyles fires time')(stains=20, seagulls=True, windows=20, gargoyles=False, fires=0, time=25)
level2 = namedtuple('literal', 'stains seagulls windows gargoyles fires time')(stains=10, seagulls=False, windows=24, gargoyles=True, fires=10, time=25)
level3 = namedtuple('literal', 'stains seagulls windows gargoyles fires time')(stains=30, seagulls=True, windows=25, gargoyles=True, fires=12,  time=40)
level_settings.append(level1)
level_settings.append(level2)
level_settings.append(level3)


towerPlatforms = []
towerWindowsDirty = []    
towerStartLocationY = 100
towerStartLocationX = 460
numberOfWindowRows = 5   # the maximum number of both window rows and columns
windowPositionOffsetX = 90   # horizontal distance between windows
windowPositionOffsetY = 150  # vertical distance between windows
towerWindows = []

stainArray = [] 

firesArray=[]
# due to there being a lower number of flames, I have set there y locations to a fixed location instead of 
# running through an algorithm which gives them a position based on a physical x and y
firesYLocations = [100, 300, 500, 700, 100, 300, 500, 700, 130, 300, 470, 600]


pabloMoveAmount = 2   # pablo's speed
