# IEatSpaceRocks, 11/09/2026


# SETUP


import pygame, random, os, pygame.freetype, math                              # Import libraries
os.chdir(os.path.dirname(os.path.abspath(__file__)))                    # Changing the directory to the folder that contains 'sorting-algorithms.py'
pygame.init()                                                           # Initialize Pygame

# Create a list and shuffle it
list = [[], []]                                                         # The list contains 2 lists, the first is the main list, the second is the saved list, if there is one
for i in range(100):                                                    # 100 items in list, values 1 to 100
    list[0].append(i + 1)
random.shuffle(list[0])                                                 # Shuffle the list

# Set up screen
width, height = 1000, 800                                               # Recommended screen size, can be changed
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

def drawToolbar(text):
    
    # Draw toolbar and buttons
    pygame.draw.rect(screen, (112, 128, 144), (0, 0, width, 50))            # Toolbar itself
    pygame.draw.rect(screen, (194, 194, 209), (0, 46, width, 5))            # Separator line
    pygame.draw.rect(screen, (48, 60, 76), (163, 7, width - 209, 32))       # Toolbar text background
    for button in buttons:
        screen.blit(button["image"], button["rect"])                        # Buttons
    
    # Draw toolbar text
    rect = font.get_rect(text[-1])
    rect.center = ((width - 209) / 2 + 163, 23)
    font.render_to(screen, rect, text[-1], (255, 255, 235))


def drawColumns(highlight):
    count = 0
    for col in list[0]:                     # Go through each value
        if col in highlight:
            colour = (255, 255, 235)        # If highlighted, use different colour
        else:
            colour = (242, 166, 94)
        pygame.draw.rect(screen, colour, (width / 100 * count, height - (height-51) / 100 * col, width / 100, height))      # Draw a column
        count += 1


def settingsPlaces(scroll):                                                       # Used for calculating places for the buttons in the settings menu
    rects = []                                                              # Empty rects list
    numx = int((width - 14) / (250 + 14))                                   # Calculate how many rectangles fit in a row, if a rectangle is at least 250 wide
    wide = (width - 14 * (numx + 1)) / numx                                 # Based on numx, how wide can a rectangle be
    high = 32                                                               # Create a list of all rect values that a rectangle can take on the setting menu
    for y in range(math.ceil(len(algorithms) / numx)):
        for x in range(numx):
            rects.append((14 + x * (wide + 14), 14 + y * (high + 14) + 50 + scroll * 46, wide, high))
    return rects                                                            # Return this list


def drawSettings(scroll):
    screen.blit(exit, exit.get_rect(topleft=(width - 39, 7)))               # Draw exit button over the settings one
    rects = settingsPlaces(scroll)                                          # Get the valid rect values for buttons to be at
    buttons = []                                                            # Store each buttons rect value in this list
    for i in range(len(algorithms)):
        rect = rects[i]
        text = algorithms[i]["name"]
        text_rect = font.get_rect(text)
        text_rect.center = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)
        pygame.draw.rect(screen, (200, 200, 200), rect)                     # Draw button
        font.render_to(screen, text_rect, text, (0, 0, 0))                  # Draw text
        buttons.append(pygame.Rect(rect))                                   # Add rect value to list
    return buttons   
            
# Sorting Algorithms

def loopHandling(highlight, assign, compare):                                                # Same loophandling to be easily used in every sorting algorithms function
    
    screen.fill((39, 39, 54))
    drawToolbar([f"Assigns: {assign} | Comparisons: {compare}"])                                                           # Clear screen, draw toolbar
    screen.blit(exit, exit.get_rect(topleft=(width - 39, 7)))               # Add exit button
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons[4]["rect"].collidepoint(event.pos):                  # Exit button functionality
                return False
    drawColumns(highlight)                                                  # Draw columns, with highlighting currently moved ones
    pygame.display.flip()                                                   # Update screen
    return True                                                             # Keep running, if not exited


def selectionSort(list):                                                    # Selection sort: (DOCUMENTATION!)

    assign, compare = 0, 0
    
    n = len(list)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if list[j] < list[min_index]:
                min_index = j
            compare += 1
        if list[i] != list[min_index]:
            list[i], list[min_index] = list[min_index], list[i]
            assign += 3
        
        
        running = loopHandling([list[min_index], list[i]], assign, compare)                   # Loophandling and framerate
        if not running:
            return f"Assigns: {assign} | Comparisons: {compare}"
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
    },
]

settings_rects = []      # List of rect values for the buttons in settings menu
text_timer = 0           # Timer for displaying temporary toolbar text for the right amount of time
selected_algo = None     # Int value that represents the place of the selected sorting algorithm in the 'algorithms' list
scroll = 0
scrolled = 0


# MAIN LOOP


running = True
while running:

    # Get current screen dimensions
    width, height = screen.get_size()
    
    # Update button/hitbox positions
    buttons[4]["rect"] = settings.get_rect(topleft=(width - 39, 7))             # Settings button
    
    scrolled = 0
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                           # Exit game if X is pressed
            running = False
        elif event.type == pygame.MOUSEWHEEL and mode == "settings":
            if event.y == -1:
                if height < (settings_rects[-1][1] + 32 - scrolled * 46):
                    scroll -= 1
                    scrolled += 1
            if event.y == 1:
                scroll += 1
                if scroll > 0:
                    scroll = 0
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:        # Check if lmb is pressed
            
            if mode == "settings" and settings_rects != []:                                              # Settings menu
                for i in range(len(settings_rects)):
                    if settings_rects[i].collidepoint(event.pos):               # If a sorting method is selected:
                        toolbar_text[0] = f"{algorithms[i]["name"]} sort"       # Add it to permanent toolbar text and selected_algo
                        selected_algo = i
                        
            for button in buttons:
                if button["rect"].collidepoint(event.pos):                      # Check if any toolbar button was pressed
                    
                    if button["image"] == settings:                             # If it was the setting/exit button:
                        if mode == "settings":
                            mode = "main"
                        else:
                            scroll = 0
                            mode = "settings"
                            toolbar_text[0] = "Settings"
                            
                    elif button["image"] == play:                               # If it was the play button:
                        if selected_algo == None:
                            toolbar_text.append("No algorithm selected!")
                            text_timer = 0
                        else:
                            toolbar_text.append(algorithms[selected_algo]["action"](list[0]))
                            text_timer = -20
                            mode = "main"
                            
                    else:                                                       # Otherwise:
                        toolbar_text.append(button["text"])
                        text_timer = 0
                        mode = "main"
                        button["action"]()                                      # Preform button action


    if len(toolbar_text) > 1:                                                   # Handle temporary and permanent toolbar texts
        if text_timer > 40:
            toolbar_text = [toolbar_text[0]]
        text_timer += 1
        
    if mode == "main":
        if selected_algo == None:
            toolbar_text[0] = "Sorting Algorithms"
        else:
            toolbar_text[0] = f"{algorithms[selected_algo]["name"]} sort"
        
    # Draw the appropriate screen
    screen.fill((39, 39, 54))
    if mode == "main":
        drawColumns([])
    else:
        settings_rects = drawSettings(scroll)
    drawToolbar(toolbar_text)

    # Update screen
    pygame.display.flip()
    pygame.time.Clock().tick(20)

# Quit pygame
pygame.quit() 
