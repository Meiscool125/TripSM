import pygame
import time
from tkinter import Tk, filedialog
from displayScene import *
import random
import os
import shutil
from datetime import datetime


def pruneSaveFileNames(allFoundSaveFiles):
    prunedList = []
    for file in allFoundSaveFiles:
        newFileName = file.split("_")[0]
        if newFileName in prunedList:
            continue
        else:
            prunedList.append(newFileName)
    print(f'pruned list:{prunedList}\n')
    return prunedList

def makeFileNameButtons(prunedList, font, color, size):
    fileButtonList = []
    y = 200
    print("File names:")
    for name in prunedList:
        print(name)
        fileButton = UsmanButton(name, font, color, (700 // 2, y), size, "Main Menu")
        y += 30
        fileButtonList.append(fileButton)
    print("\n")
    return fileButtonList

def makeFullPathToFile(root,file,returnFilePath):
    file_path = os.path.join(root, file)
    if returnFilePath:
        return file_path
    
    # Use os.path.basename to get the filename from the full path
    filename = os.path.basename(file_path)
    print(filename)
    return filename

def getSaveFilePaths(filePathToSaves):
    allFoundSaveFileNames = []
    files = os.listdir(filePathToSaves)
    for file in files:
        if file.endswith(".sav"):
            allFoundSaveFileNames.append(file)
    print(f'All found saves: {allFoundSaveFileNames}\n')
    return allFoundSaveFileNames


"""
    allFoundSaveFiles = []
    for root, dirs, files in os.walk(filePathToSaves):
        for file in files:
            if file[-4:] == ".sav":  # make sure were only selecting save files
                filename = makeFullPathToFile(root,file,False)
                allFoundSaveFiles.append(filename)
    print(allFoundSaveFiles)
    return allFoundSaveFiles
"""

def openFileBrowser(browserTitle):
    root = Tk()
    root.withdraw()  # Hide the main window
    filePath = filedialog.askdirectory(title=browserTitle)
    # print("Selected folder:", filePathToSaves)
    return filePath

def deleteSave(saveToDelete):
    try:  # try to delete the save
        os.remove(saveToDelete)
        # print(f'wouldve deleted: {saveToDelete}')
    except FileNotFoundError as exception:
        scene = "Main Menu"
        print(f"File not found. Error: {exception}")
    except Exception as exception:
        scene = "Main Menu"
        print(exception)
        
def changeButtonColorWhenHoveringOverIt():
    for button in buttonGroup.sprites():
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            button.color = gray
        else:
            button.color = white
            
def renderButtons(screen,scene):
    for button in buttonGroup.sprites():
        if scene == button.scene:
            #pygame.draw.rect(screen, white, button.rect) #TOGGLE THIS LINE TO SEE BUTTONS HITBOXES
            button.rerenderText()
            textRect = button.textToBlit.get_rect(center=button.pos)
            screen.blit(button.textToBlit, textRect)

def findButtonSceneThing(event,scene):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
        print(f'Current Scene: {scene}\n')
        for button in buttonGroup.sprites():
            if scene == button.scene:
                print(f'Found a button in scene: "{scene}"\n')
                
def remakeFileButtonList(prunedList,allFoundSaveFiles,filePathToSaves,):
    for button in buttonGroup.sprites():
        if button.text in prunedList:
            button.kill()
    allFoundSaveFiles = getSaveFilePaths(filePathToSaves)  # get the file paths of each individual save
    prunedList = pruneSaveFileNames(allFoundSaveFiles)  # prune the file paths down to just the names so that we can put it in a UI
    fileButtonList = makeFileNameButtons(prunedList, smallFont, white, (215, 50))
    
def successScene(successTime, currentTime):
    if (round(currentTime) - round(successTime)) > 3:
        print("did it")
        return True
    
def extractTimestamp(filename):
    # Extract timestamp from filename
    timestamp_str = filename.split('_')[-1].split('.')[0]
    # Convert timestamp to datetime object
    return datetime.strptime(timestamp_str, "%d%m%y-%H%M%S")

def willMakeError(file):
    if "autosave" in file:
        return "Error"
    if file.count("_") > 1:
        return "Error"
    if file.count(".") > 1:
        return "Error"
    return "No Error"

def deleteMultipleSaves(fileList,fileToEdit,filePathToSaves):
    for file in fileList:  # list with paths to save file
        if file[:len(fileToEdit)] == fileToEdit:  # is this a save we need to delete?
            saveToDelete = f'{filePathToSaves}/{file}'  # recreate file path for deletion
            deleteSave(saveToDelete)

def getAllOfOneSave(fileList,fileToEdit,ignoreErrors):
    list = []
    for file in fileList:
        if file[:len(fileToEdit)] == fileToEdit:
            isError = willMakeError(file)
            if isError == "Error" and not ignoreErrors:
                print(f'File "{file}" will NOT used in save backing up, as it will mess up the program.')
            else:
                list.append(file)
    return list

def backupSaveFile(sortedFilenamesByTime,filePathToSaves):
    backupFolder = openFileBrowser("Select a folder to backup this save to")
    if backupFolder == "":
        return False
    mostRecentSaveFile = sortedFilenamesByTime[-1]
    mostRecentSaveFilePath = makeFullPathToFile(filePathToSaves, mostRecentSaveFile, True)
    backupFilePath = makeFullPathToFile(backupFolder, mostRecentSaveFile, True)
    shutil.copy(mostRecentSaveFilePath, backupFilePath)
    return True
def attemptFileSortByTime(allOfOneSaveList):
    try:
        sortedFilenamesByTime = sorted(allOfOneSaveList, key=extractTimestamp)
        return sortedFilenamesByTime
    except Exception as exception:
        print(f'Error: {exception}')
        scene = "Main Menu"

def deleteOldSaves(sortedFilenamesByTime, filePathToSaves):
    for save in sortedFilenamesByTime:
        if save != sortedFilenamesByTime[-1]:
            save = makeFullPathToFile(filePathToSaves, save, True)
            deleteSave(save)
    