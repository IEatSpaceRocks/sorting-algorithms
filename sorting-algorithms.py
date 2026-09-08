# IEatSpaceRocks, 08/09/2026


# SETUP


import pygame, random, os, pygame.freetype                              # Import libraries
os.chdir(os.path.dirname(os.path.abspath(__file__)))                    # Changing the directory to the folder that contains 'sorting-algorithms.py'
pygame.init()                                                           # Initialize Pygame

# Create a list and shuffle it
list = [[], []]                                                         # The list contains 2 lists, the first is the main list, the second is the saved list, if there is one
for i in range(100):                                                    # 100 items in list, values 1 to 100
    list[0].append(i + 1)
random.shuffle(list[0])                                                 # Shuffle the list

# Set up screen
width, height = 600, 800                                                # Recommended screen size, can be changed
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)     # Create screen, resizable
pygame.display.set_caption("Sorting Algorithms")                        # Name window 'Sorting Algorithms

# Set up text and mode
font = pygame.freetype.Font(None, 30)                                   # Define font to be used
toolbar_text = ["Sorting Algorithms"]                                    # Text to be displayed on toolbar. Format: [main text, temporary text]
mode = "main"                                                           # Mode for the program (main, settings)

# Load images
def loadImage(name):
    return pygame.image.load(f"assets/{name}").convert()                # Take images from assets folder
save = loadImage("save.png")
load = loadImage("load.png")
shuffle = loadImage("shuffle.png")
play = loadImage("play.png")
settings = loadImage("settings.png")
exit = loadImage("exit.png")


# Buttons

def saveBtn():                              # Used for saving the main list. Only 1 list can be saved at once
    list[1] = []                            # Empty current saved list
    for item in list[0]:                    # Add all elements of the main list to the new saved list
        list[1].append(item)         
    
    
def loadBtn():                              # Used for loading in the saved list instead of the current main list
    if list[1] != []:                       # If there is a saved list:
        list[0] = []                        # Empty main list
        for item in list[1]:                # Add all elements of the saved list to the main list
            list[0].append(item)            
    else:                                   # If there isn't a saved list:
        toolbar_text.pop()                  # Don't change toolbar text
        
        
def shuffleBtn():                           # Used for shuffling the main list
    random.shuffle(list[0])                 # Shuffle main list
        
        
# Set up buttons
buttons = [
    {
        "image": save,
        "text": "Saved current list",
        "rect": save.get_rect(topleft=(7, 7)),
        "action": saveBtn,
    },
    {
        "image": load,
        "text": "Loaded in saved list",
        "rect": load.get_rect(topleft=(46, 7)),
        "action": loadBtn,
    },
    {
        "image": shuffle,
        "text": "Shuffled current list",
        "rect": shuffle.get_rect(topleft=(85, 7)),
        "action": shuffleBtn,
    },
    {
        "image": play,
        "rect": play.get_rect(topleft=(124, 7)),
    },
    {
        "image": settings,
        "rect": settings.get_rect(topleft=(width - 39, 7)),
    },
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
    rect = font.get_rect(toolbar_text[-1])
    rect.center = ((width - 209) / 2 + 163, 23)
    font.render_to(screen, rect, toolbar_text[-1], (255, 255, 235))


def drawColumns(highlight):
    count = 0
    for col in list[0]:                     # Go through each value
        if col in highlight:
            colour = (255, 255, 235)        # If highlighted, use different colour
        else:
            colour = (242, 166, 94)
        pygame.draw.rect(screen, colour, (width / 100 * count, height - (height-51) / 100 * col, width / 100, height))      # Draw a column
        count += 1


def settingsPlaces():                                                       # Used for calculating places for the buttons in the settings menu
    rects = []                                                              # Empty rects list
    numx = int((width - 14) / (250 + 14))                                   # Calculate how many rectangles fit in a row, if a rectangle is at least 250 wide
    numy = int((height - 50 - 14) / (32 + 14))                              # Calculate how many rectangles fit in a column, if a rectangle is at least 32 high
    if numx == 0 or numy == 0:                                              # If there isn't space for any buttons, return an empty list
        return []
    wide = (width - 14 * (numx + 1)) / numx                                 # Based on numx, how wide can a rectangle be
    high = (height - 50 - 14 * (numy + 1)) / numy                           # Based on numy, how high can a rectangle be
    for y in range(numy):                                                   # Create a list of all rect values that a rectangle can take on the setting menu
        for x in range(numx):                                               # Format of list: row1col1, row1col2, row1col3... row2col1, row2col2...
            rects.append((14 + x * (wide + 14), 14 + y * (high + 14) + 50, wide, high))
    return rects                                                            # Return this list


def drawSettings():
    screen.blit(exit, exit.get_rect(topleft=(width - 39, 7)))               # Draw exit button over the settings one
    rects = settingsPlaces()                                                # Get the valid rect values for buttons to be at
    count = 0                                                               # Count how many buttons are drawn in the settings menu
    buttons = []                                                            # Store each buttons rect value in this list
    for rect in rects:
        if count == len(algorithms):                                        # If there are already enough buttons for displaying all sorting types:
            return buttons                                                      # Return a list of their rect values
        text = algorithms[count]["name"]                                    # Name of sorting algorithm
        text_rect = font.get_rect(text)
        text_rect.center = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)
        pygame.draw.rect(screen, (200, 200, 200), rect)                     # Draw button
        font.render_to(screen, text_rect, text, (0, 0, 0))                  # Draw text
        buttons.append(pygame.Rect(rect))                                   # Add rect value to list
        count +=1
            
            
# Sorting Algorithms

def loopHandling(highlight):                                                # Same loophandling to be easily used in every sorting algorithms function
    
    drawToolbar()                                                           # Clear screen, draw toolbar
    screen.blit(exit, exit.get_rect(topleft=(width - 39, 7)))               # Add exit button
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons[4]["rect"].collidepoint(event.pos):                  # Exit button functionality
                return False
    drawColumns(highlight)                                                  # Draw columns, with highlighting currently moved ones
    pygame.display.flip()                                                   # Update screen
    return True                                                             # Keep running, if not exited


def selectionSort(list):                                                    # Selection sort: (DOCUMENTATION!)
    
    n = len(list)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if list[j] < list[min_index]:
                min_index = j
        list[i], list[min_index] = list[min_index], list[i]
        
        
        running = loopHandling([list[min_index], list[i]])                   # Loophandling and framerate
        if not running:
            return
        pygame.time.Clock().tick(20)
    
    
algorithms = [
    {
        "name": "Selection",
        "action": selectionSort
    },
    {
        "name": "Bubble",
        "action": ""
    },
    {
        "name": "Cocktail shaker",
        "action": ""
    }
]

settings_rects = []      # List of rect values for the buttons in settings menu
text_timer = 0           # Timer for displaying temporary toolbar text for the right amount of time
selected_algo = None     # Int value that represents the place of the selected sorting algorithm in the 'algorithms' list


# MAIN LOOP


running = True
while running:

    # Get current screen dimensions
    width, height = screen.get_size()
    
    # Update button/hitbox positions
    buttons[4]["rect"] = settings.get_rect(topleft=(width - 39, 7))             # Settings button
    
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                           # Exit game if X is pressed
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:        # Check if lmb is pressed
            
            if mode == "settings":                                              # Settings menu
                for i in range(len(settings_rects)):
                    if settings_rects[i].collidepoint(event.pos):               # If a sorting method is selected:
                        toolbar_text[0] = f"{algorithms[i]["name"]} sort"       # Add it to permanent toolbar text and selected_algo
                        selected_algo = i
                        
            for button in buttons:
                if button["rect"].collidepoint(event.pos):                      # Check if any toolbar button was pressed
                    
                    if button["image"] == settings:                             # If it was the setting/exit button:
                        if mode == "settings":
                            mode = "main"
                            if selected_algo == None:
                                toolbar_text[0] = "Sorting Algorithms"
                            else:
                                toolbar_text[0] = f"{algorithms[selected_algo]["name"]} sort"
                        else:
                            toolbar_text[0] = "Settings"
                            mode = "settings"
                            
                    elif button["image"] == play:                               # If it was the play button:
                        if selected_algo == None:
                            toolbar_text.append("No algorithm selected!")
                            text_timer = 0
                        else:
                            algorithms[selected_algo]["action"](list[0])
                            mode = "main"
                            
                    else:                                                       # Otherwise:
                        toolbar_text.append(button["text"])
                        text_timer = 0
                        mode = "main"
                        button["action"]()                                      # Preform button action


    if len(toolbar_text) > 1:                                                   # Handle temporary and permanent toolbar texts
        if text_timer > 12:
            toolbar_text = [toolbar_text[0]]
        text_timer += 1
        
    # Draw the appropriate screen
    drawToolbar()
    if mode == "main":
        drawColumns([])
    elif mode == "settings":
        settings_rects = drawSettings()

    # Update screen
    pygame.display.flip()
    pygame.time.Clock().tick(6)

# Quit pygame
pygame.quit() 
