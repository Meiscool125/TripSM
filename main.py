# get important stuff in
from functions import *


# pygame.init starts the code
pygame.init()

# create time
clock = pygame.time.Clock()
startTime = pygame.time.get_ticks()/1000
currentTime = pygame.time.get_ticks()/1000 - startTime

# set variables
CurrentlyRunning = True
filePathToSaves = None
showPleaseSelectFolderText = False
mouseAlreadyDown = False
allFoundSaveFiles = []
prunedList = []
saveFolderSelected = False
button = None
mostRecentlyClickedButton = None

# screen setup
screen = pygame.display.set_mode((700, 700))

# make bg color incase img fails to load
screen.fill((0, 0, 0))

# make console look nicer
print("\n")

# make the name of the window
pygame.display.set_caption('Simple Satisfactory Save Manager')

# set the scene (literally) (im funny asf)
scene = "Introduction"

# making buttons
continueButton1 = UsmanButton('Continue', bigFont, white, (700 // 2,290), (215, 50), "Introduction")
openFileBrowserButton1 = UsmanButton('Open File Browser', mediumFont, white, (700 // 2,280), (215, 50), "Enter Satisfactory Path")
backButton = UsmanButton('Back to Main Menu™', smallFont, white, (150,670), (100, 50), "Specific File Managing")
deleteButton = UsmanButton('Delete all instances of this save file', smallFont, white, (700 // 2, 100), (100, 50), "Specific File Managing")
backupButton = UsmanButton('Backup the most recently made save file', smallFont, white, (700 // 2, 150), (100, 50), "Specific File Managing")
deleteOldSavesButton = UsmanButton('Keep the most recent save and delete older files', smallFont, white, (700 // 2, 200), (100, 50), "Specific File Managing")

while CurrentlyRunning:

    #setting what "time" it is in milliseconds
    currentTime = pygame.time.get_ticks() / 1000 - startTime

    #filling the screen with a grey color
    screen.fill((128,128,128))

    # using function from displayScene.py to show text onscreen
    displaySceneText(scene,screen,filePathToSaves,mostRecentlyClickedButton)

    # extra text that can popup
    if showPleaseSelectFolderText == True and scene == "Enter Satisfactory Path":
        blitText("Please select a folder!", mainFont, black, (700 // 2, 350), screen, True)
    if scene == "Success Scene":
        if successScene(successTime, currentTime) == True:
            scene = "Main Menu"

    #event handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # user clicked close button
            CurrentlyRunning = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # check if user clicked LMB
            for button in buttonGroup.sprites(): # Check if any (coded) button was clicked
                if button.rect.collidepoint(event.pos) and not mouseAlreadyDown and scene == button.scene: #so we clicked a button but should it run code?
                    mouseAlreadyDown = True
                    print(f'Clicked button: "{button.text}"\n') #what button did we click on?
                    # making each button do its own thing
                    if scene == button.scene: # makes it so that we can skip unnecessary coding
                        print(f'Ran code for button: "{button.text}"\n') #what button did we run code for?
                        mostRecentlyClickedButton = button

                        if button == continueButton1: #IF THERE IS TROUBLE ADD (and scene == "Introduction")
                            scene = "Enter Satisfactory Path"

                        elif button == openFileBrowserButton1:
                            filePathToSaves = openFileBrowser("Select the folder containing all Satisfactory Saves") # get file path to saves
                            # potentially activate PleaseSelectFolderText
                            if filePathToSaves == "":
                                showPleaseSelectFolderText = False
                            if not showPleaseSelectFolderText:
                                showPleaseSelectFolderText = True

                            if filePathToSaves is not None and filePathToSaves != "": # if we have a real path to the saves
                                scene = "Main Menu"
                                allFoundSaveFiles = getSaveFilePaths(filePathToSaves) # get the file paths of each individual save
                                prunedList = pruneSaveFileNames(allFoundSaveFiles) # prune the file paths down to just the names so that we can put it in a UI


                        if scene == "Main Menu":
                            # make buttons for all files
                            if not saveFolderSelected:
                                saveFolderSelected = True
                                fileButtonList = makeFileNameButtons(prunedList,smallFont, white, (215,50))

                            if button.text in prunedList: # is the button we clicked on one of the save file names?
                                fileToEdit = button.text
                                scene = "Specific File Managing"

                        if scene == "Specific File Managing":
                            if button == backButton: # back to main menu button
                                scene = "Main Menu"

                            if button == deleteButton: # delete all of that save file button
                                deleteMultipleSaves(allFoundSaveFiles,fileToEdit,filePathToSaves)
                                remakeFileButtonList(prunedList,allFoundSaveFiles,filePathToSaves)
                                currentTime = pygame.time.get_ticks() / 1000 - startTime
                                successTime = currentTime
                                scene = "Success Scene"

                            if button == backupButton: #backup most recent file of a save group
                                allOfOneSaveList = getAllOfOneSave(allFoundSaveFiles,fileToEdit,False)
                                sortedFilenamesByTime = attemptFileSortByTime(allOfOneSaveList)
                                backupSaveFile(sortedFilenamesByTime,filePathToSaves)
                                currentTime = pygame.time.get_ticks() / 1000 - startTime
                                successTime = currentTime
                                scene = "Success Scene"

                            if button == deleteOldSavesButton: # take a guess
                                allOfOneSaveList = getAllOfOneSave(allFoundSaveFiles,fileToEdit,False)
                                sortedFilenamesByTime = attemptFileSortByTime(allOfOneSaveList)
                                deleteOldSaves(sortedFilenamesByTime, filePathToSaves)
                                remakeFileButtonList(prunedList,allFoundSaveFiles,filePathToSaves)
                                currentTime = pygame.time.get_ticks() / 1000 - startTime
                                successTime = currentTime
                                scene = "Success Scene"
        # making sure that buttons cant be clicked too many times a second
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouseAlreadyDown = False
            for button in buttonGroup.sprites():
                if button.rect.collidepoint(event.pos) and button.clicked == True:
                    button.clicked = False

        # random thing
        findButtonSceneThing(event,scene)
    changeButtonColorWhenHoveringOverIt()
    renderButtons(screen,scene)

    #set FPS max to 30
    clock.tick(30)
    # update the display
    pygame.display.flip()
pygame.quit()
