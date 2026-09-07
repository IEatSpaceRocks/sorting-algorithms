# IEatSpaceRocks, 07/09/2026


# SETUP

import pygame, random, os, pygame.freetype              # Import libraries
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # Changing the directory to the folder that contains 'sorting-algorithms.py'
pygame.init()                                           # Initialize Pygame

# Create a list and shuffle it
list = [[], []]                                         # The list contains 2 lists, the first is the main list, the second is the saved list, if there is one
for i in range(100):                                    # 100 items in list, values 1 to 100
    list[0].append(i + 1)
random.shuffle(list[0])                                 # Shuffle the list

# Set up screen
width, height = 600, 800                                                # Recommended screen size, can be changed
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)     # Create screen, resizable
pygame.display.set_caption("Sorting Algorithms")                        # Name window 'Sorting Algorithms

# Set up text and mode
font = pygame.freetype.Font(None, 30)       # Define font to be used
toolbarText = "Sorting Algorithms"          # Text to be displayed on toolbar
mode = "main"                               # Mode for the program (main, settings, sorting)

# Load images
def loadImage(name):
    return pygame.image.load(f"assets/{name}").convert()    # Take images from assets folder
save = loadImage("save.png")
load = loadImage("load.png")
shuffle = loadImage("shuffle.png")
play = loadImage("play.png")
settings = loadImage("settings.png")
exit = loadImage("exit.png")


# Buttons

def saveBtn():                      # Used for saving the main list. Only 1 list can be saved at once
    list[1] = []                        # Empty current saved list
    for item in list[0]:                # Add all elements of the main list to the new saved list
        list[1].append(item)
    return "Saved", "main"              
    
    
def loadBtn():                      # Used for loading in the saved list instead of the current main list
    if list[1] != []:                   # If there is a saved list:
        list[0] = []                        # Empty main list
        for item in list[1]:                # Add all elements of the saved list to the main list
            list[0].append(item)
        return "Loaded", "main"             
    else:                               # If there isn't a saved list:
        return toolbarText, mode            # Don't change toolbar text or mode (= do nothing)
        
        
def shuffleBtn():                   # Used for shuffling the main list
    random.shuffle(list[0])             # Shuffle main list
    return "Shuffled", "main"
    
    
def playBtn():
    selection_sort(list[0])
    return "Sorted", "main"
    
    
def settingsBtn():                  # Used either for accessing or leaving settings menu
    if mode == "settings":                  # If settings is already open:
        return "Sorting Algorithms", "main"     
    else:                                   # If it isn't:
        return "Settings", "settings"


# Set up buttons
buttons = [
    {
        "image": save,
        "rect": save.get_rect(topleft=(7, 7)),
        "action": saveBtn,
    },
    {
        "image": load,
        "rect": load.get_rect(topleft=(46, 7)),
        "action": loadBtn,
    },
    {
        "image": shuffle,
        "rect": shuffle.get_rect(topleft=(85, 7)),
        "action": shuffleBtn,
    },
    {
        "image": play,
        "rect": play.get_rect(topleft=(124, 7)),
        "action": playBtn,
    },
    {
        "image": settings,
        "rect": settings.get_rect(topleft=(width - 39, 7)),
        "action": settingsBtn,
    },
]

algorithms = [
    {
    
    }
]


# Visual functions

def drawToolbar():
    # Clear screen
    screen.fill((39, 39, 54))
    
    # Draw toolbar and buttons
    pygame.draw.rect(screen, (112, 128, 144), (0, 0, width, 50))            # Toolbar itself
    pygame.draw.rect(screen, (194, 194, 209), (0, 46, width, 5))            # Separator line
    pygame.draw.rect(screen, (48, 60, 76), (163, 7, width - 209, 32))       # Toolbar text background
    for button in buttons:
        screen.blit(button["image"], button["rect"])                        # Buttons
    
    # Draw toolbar text
    rect = font.get_rect(toolbarText)
    rect.center = ((width - 209) / 2 + 163, 23)
    font.render_to(screen, rect, toolbarText, (255, 255, 235))


def drawColumns(highlight):
    count = 0
    for col in list[0]:                     # Go through each value
        if col in highlight:
            colour = (255, 255, 235)        # If highlighted, use different colour
        else:
            colour = (242, 166, 94)
        pygame.draw.rect(screen, colour, (width / 100 * count, height - (height-51) / 100 * col, width / 100, height))      # Draw a column
        count += 1


def settingsPlaces():                                               # Used for calculating places for the buttons in the settings menu
    rects = []                                                      # Empty rects list
    numx = int((width - 14) / (250 + 14))                           # Calculate how many rectangles fit in a row, if a rectangle is at least 250 wide
    numy = int((height - 50 - 14) / (32 + 14))                      # Calculate how many rectangles fit in a column, if a rectangle is at least 32 high
    wide = (width - 14 * (numx + 1)) / numx                         # Based on numx, how wide can a rectangle be
    high = (height - 50 - 14 * (numy + 1)) / numy                   # Based on numy, how high can a rectangle be
    for y in range(numy):                                               # Create a list of all rect values that a rectangle can take on the setting menu
        for x in range(numx):                                           # Format of list: row1col1, row1col2, row1col3... row2col1, row2col2...
            rects.append((14 + x * (wide + 14), 14 + y * (high + 14) + 50, wide, high))
    return rects                                                    # Return this list

def drawSettings():
    screen.blit(exit, exit.get_rect(topleft=(width - 39, 7)))               # Draw exit button over the settings one
    rects = settingsPlaces()                                                # Get the valid rect values for buttons to be at
    for rect in rects:
        text_rect = font.get_rect("Hello")
        text_rect.center = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)
        pygame.draw.rect(screen, (200, 200, 200), rect)
        font.render_to(screen, text_rect, "Hello", (0, 0, 0))
            
def selection_sort(arr):
    n = len(arr)

    for i in range(n - 1):
        min_index = i

        # Find the smallest element in the unsorted portion
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        # Place it at the beginning of the unsorted portion
        arr[i], arr[min_index] = arr[min_index], arr[i]
         
        drawToolbar()
        drawColumns([arr[min_index], arr[i]])
        pygame.display.flip()
        pygame.time.Clock().tick(6)
    
    

# MAIN LOOP

running = True
while running:
    
    # Get current screen dimensions
    width, height = screen.get_size()
    
    # Update button/hitbox positions
    buttons[4]["rect"] = settings.get_rect(topleft=(width - 39, 7))         # Settings button
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                       # Exit game if X is pressed
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    # Check if lmb is pressed
            for button in buttons:
                if button["rect"].collidepoint(event.pos):                  # Check if any button was pressed
                    if button["action"] == play:
                        main = "sorting"
                    toolbarText, mode = button["action"]()                        # Preform button action

    
    drawToolbar()
    
    if mode == "main":
        drawColumns([])
    
    elif mode == "settings":
        drawSettings()
        
    elif mode == "sorting":
        pass

    # Update screen
    pygame.display.flip()
    pygame.time.Clock().tick(6)

pygame.quit() 
