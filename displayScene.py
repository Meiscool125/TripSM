import pygame
pygame.init()

# setting vars
buttonGroup = pygame.sprite.Group()
bigFont = pygame.font.Font("fonts/onyx.ttf", 70)
bigFontNormalText = pygame.font.Font(None, 70)
mediumFont = pygame.font.Font("fonts/onyx.ttf", 35)
mainFont = pygame.font.Font(None, 46)
smallFont = pygame.font.Font(None, 40)
miniFont = pygame.font.Font(None, 34)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

# func to show text on screen
def blitText(text,font,color,pos,screen,centered):
    textToBlit = font.render(text,True,color)
    textRect = textToBlit.get_rect(center=pos)
    if not centered:
        screen.blit(textToBlit, pos)
    elif centered:
        screen.blit(textToBlit, textRect) #700x700 is screen size

# func to show text on screen but thick (maybe for like warnings?)
def blitThickText(text,font,color,pos,screen,centered):
    textToBlit = font.render(text,True,color)
    textRect = textToBlit.get_rect(center = pos) #700x700 is screen size
    #failed attempt at outlining the text
    """
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        outlineRect = textRect.move(dx,dy)
        screen.blit(textSurface,outlineRect)
    """
    #centering
    if not centered:
        screen.blit(textToBlit, pos)
    elif centered:
        screen.blit(textToBlit, textRect)  # 700x700 is screen size

# called UsmanButton and not Button because my teacher taught me how to make this type of button
class UsmanButton(pygame.sprite.Sprite):
    def __init__(self,text,font,color,pos,size,scene):
        super().__init__()
        self.text = text
        self.font = font
        self.color = color
        self.pos = pos
        self.size = self.font.size(self.text)
        self.scene = scene
        self.textToBlit = font.render(self.text,True,self.color)
        self.clicked = False
        self.rect = self.textToBlit.get_rect(center=self.pos)
        self.rect.size = self.size
        buttonGroup.add(self)
    def rerenderText(self):
        self.textToBlit = self.font.render(self.text, True, self.color)

# scene is set, so start the show!
def displaySceneText(scene,screen,filePathToSaves,mostRecentlyClickedButton):
    if scene == "Introduction":
        blitText("Ficsit™ welcomes you to the", mainFont, black, (700 // 2,120),screen, True)
        blitText("Simple Satisfactory Save Manager™!", mainFont, black, (700 // 2,150), screen, True)
        blitText("Copyright by meiscool125 ©", mainFont, black, (700 // 2, 680), screen, True) #please dont change this line and redistribute it. its fine if you redistribute but just dont change it to something else :D
        blitText("Notes:", smallFont, black, (700 // 2, 400), screen, True)
        blitText("Make sure your save file names ", smallFont, black, (700 // 2, 425), screen, True)
        blitText("only have ONE underscore", smallFont, black, (700 // 2, 450), screen, True)
        blitText("and only have ONE period.", smallFont, black, (700 // 2, 475), screen, True)
    if scene == "Enter Satisfactory Path":
        blitText("Please open the folder", mainFont, black, (700 // 2,120),screen, True)
        blitText("with your Satisfactory saves.", mainFont, black, (700 // 2, 150), screen, True)
    if scene == "Main Menu":
        blitText("Ficsit Main Menu™", mainFont, black,(700 // 2, 50),screen, True)
        blitText("Select a save to manage:", mainFont, black,(700 // 2, 150),screen, True)
    if scene == "Specific File Managing":
        blitText(f'Choose an action for "{mostRecentlyClickedButton.text}":', smallFont, black,(700 // 2, 50),screen, True)
    if scene == "Success Scene":
        blitText(f'Success!', bigFontNormalText, black,(700 // 2, 300),screen, True)


# outline for how to make your very own "Usman Button™"!
'''
button object
    text
    text color
    rect
    original color
    hover color
    clicked color
    function

in your while running
    in your event loop
        in the mouse motion event type
            check collisions with all button objects
                if colliding change rect color else make it normal color
'''