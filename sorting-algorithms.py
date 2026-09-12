# IEatSpaceRocks, 12/09/2026


# SETUP


import pygame, random, os, pygame.freetype, math                        # Import libraries
os.chdir(os.path.dirname(os.path.abspath(__file__)))                    # Changing the directory to the folder that contains 'sorting-algorithms.py' and 'assets'
pygame.init()                                                           # Initialize Pygame

# Create an array and shuffle it
array = [[], []]                                                        # The array contains 2 lists, the first is the main array, the second is the saved array, if there is one
for i in range(100):                                                    # 100 items in the array, values 1 to 100
    array[0].append(i + 1)
random.shuffle(array[0])                                                # Shuffle the main array

# Set up screen
width, height = 1000, 800                                               # Recommended screen size, can be changed
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)     # Create screen, resizable
pygame.display.set_caption("Sorting Algorithms")                        # Name window 'Sorting Algorithms

# Set up text and mode
font = pygame.freetype.Font(None, 30)                                   # Define font to be used
toolbar_text = ["Sorting Algorithms"]                                   # Text to be displayed on toolbar. Format: [main text, temporary text]
mode = "main"                                                           # Current mode for the program ("main" or "settings")

# Load images
def loadImage(name):
    return pygame.image.load(f"assets/{name}").convert()                # Load images from assets folder
save = loadImage("save.png")
load = loadImage("load.png")
shuffle = loadImage("shuffle.png")
play = loadImage("play.png")
settings = loadImage("settings.png")
exit = loadImage("exit.png")


# UI


# Set up buttons
def saveBtn():                              # Used for saving the main array. Only 1 array can be saved at once
    array[1] = []                           # Empty current saved array
    for item in array[0]:                   # Add all elements of the main array to the new saved array
        array[1].append(item)         
    
def loadBtn():                              # Used for loading in the saved array instead of the current main array
    if array[1] != []:                      # If there is a saved array:
        array[0] = []                       # Empty main array
        for item in array[1]:               # Add all elements of the saved array to the main array
            array[0].append(item)            
    else:                                   # If there isn't a saved array:
        toolbar_text.pop()                  # Don't change toolbar text
        
def shuffleBtn():                           # Used for shuffling the main array
    random.shuffle(array[0])                # Shuffle main array
        

buttons = [
    {
        "image": save,
        "text": "Saved current array",
        "rect": save.get_rect(topleft=(7, 7)),
        "action": saveBtn,
    },
    {
        "image": load,
        "text": "Loaded in saved array",
        "rect": load.get_rect(topleft=(46, 7)),
        "action": loadBtn,
    },
    {
        "image": shuffle,
        "text": "Shuffled current array",
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


def drawToolbar(text):
    
    # Draw toolbar and buttons
    pygame.draw.rect(screen, (112, 128, 144), (0, 0, width, 50))            # Toolbar itself
    pygame.draw.rect(screen, (194, 194, 209), (0, 46, width, 5))            # Separator line
    pygame.draw.rect(screen, (48, 60, 76), (163, 7, width - 209, 32))       # Toolbar text background
    for button in buttons:
        screen.blit(button["image"], button["rect"])                        # Draw buttons
    
    # Draw toolbar text
    rect = font.get_rect(text[-1])
    rect.center = ((width - 209) / 2 + 163, 23)
    font.render_to(screen, rect, text[-1], (255, 255, 235))


def drawColumns(highlight):
    count = 0
    for col in array[0]:                    # Go through each value
        if col in highlight:
            colour = (255, 255, 235)        # If highlighted, use different colour
        else:
            colour = (242, 166, 94)
        pygame.draw.rect(screen, colour, (width / 100 * count, height - (height-51) / 100 * col, width / 100, height))      # Draw a column
        count += 1


def settingsPlaces(scroll):                                                 # Used for calculating places for the buttons in the settings menu
    rects = []
    numx = math.floor((width - 14) / (250 + 14))                            # Calculate how many rectangles fit in a row, if a rectangle is at least 250 wide
    if numx < 1:                                                            # Avoid division by 0 error, if screen is too narrow
        return []
    wide = (width - 14 * (numx + 1)) / numx                                 # Based on numx, how wide should a rectangle be
    high = 32
    for y in range(math.ceil(len(algorithms) / numx)):
        for x in range(numx):                                               # Create a list of all rect values that a rectangle can take on the setting menu
            rects.append((14 + x * (wide + 14), 14 + y * (high + 14) + 50 + scroll * 46, wide, high))
    return rects                                                            # Return this list


def drawSettings(scroll):
    screen.blit(exit, exit.get_rect(topleft=(width - 39, 7)))               # Draw exit button over the settings one
    rects = settingsPlaces(scroll)                                          # Get the valid rect values for buttons to be at
    if rects == []:                                                         # If screen is too narrow, can't draw buttons
        return []
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
            
            
# SORTING ALGORITHMS


def loopHandling(highlight, assign, compare):                               # Loop handling function, to be easily used in every sorting algorithms function
    
    screen.fill((39, 39, 54))                                               # Clear screen
    drawToolbar([f"Assigns: {assign} | Comparisons: {compare}"])            # Draw toolbar
    screen.blit(exit, exit.get_rect(topleft=(width - 39, 7)))               # Draw exit button
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons[4]["rect"].collidepoint(event.pos):                  # Exit button functionality
                return False
    drawColumns(highlight)                                                  # Draw columns, with highlighting currently moved ones
    pygame.display.flip()                                                   # Update screen
    return True                                                             # Keep running, if not exited


def selectionSort(array):                                                   # Selection sort

    assign, compare = 0, 0                                                  # Variables used for tracking sorting efficiency
    n = len(array)
    for i in range(n - 1):                                                  # Go through array from left to right
        min_index = i                                                       # Pick the first item of the unsorted array to be the smallest
        for j in range(i + 1, n):                                           # Go through the unsorted part of the array
            if array[j] < array[min_index]:                                 # Find the smallest item from the unsorted array
                min_index = j
            compare += 1
        if array[i] != array[min_index]:
            array[i], array[min_index] = array[min_index], array[i]         # Swap the first item of the unsorted array with the smallest
            assign += 3                                                     # Swaps count as 3 assignments. Swap A and B: A -> temp, B -> A, temp -> B
        
        running = loopHandling([array[min_index], array[i]], assign, compare)                   # Loophandling
        if not running:
            return f"Assigns: {assign} | Comparisons: {compare}"
        pygame.time.Clock().tick(20)                                                            # Framerate
    
    
def doubleSelectionSort(array):                                             # Double selection sort
    
    assign, compare = 0, 0                                                  # Variables used for tracking sorting efficiency
    n = len(array)
    for i in range(n // 2):                                                 # Go through roughly half the array (round down)
        min_index = i
        max_index = i
        for j in range(i + 1, n - i):                                       # Go through unsorted part of the array (middle)
            if array[j] < array[min_index]:                                 # Find smallest
                min_index = j
            if array[j] > array[max_index]:                                 # Find biggest
                max_index = j
            compare += 2
        if max_index == i:                                                  # If i contains the biggest item, it will be swapped to min_index, so set that as max_index
            max_index = min_index
        if i != min_index:                                                  # Swap smallest to right place
            array[i], array[min_index] = array[min_index], array[i]
            assign += 3
        if n - i - 1 != max_index:                                          # Swap biggest to right place
            array[n - i - 1], array[max_index] = array[max_index], array[n - i - 1]
            assign += 3
            
        running = loopHandling([array[min_index], array[max_index], array[i], array[n - i - 1]], assign, compare)       # Loophandling
        if not running:
            return f"Assigns: {assign} | Comparisons: {compare}"
        pygame.time.Clock().tick(20)                                                                                    # Framerate
        
        
def insertionSort(array):                                                   # Insertion sort
    
    assign, compare = 0, 0                                                  # Variables used for tracking sorting efficiency
    for i in range(1, len(array)):                                          # Go through the array from left to right, starting from the second value
        value = array[i]                                                    # Temporarily store the selected value
        assign += 1
        place = i - 1                                                       # Checked value, one before the selected
        while place >= 0:                                                   # Search from selected value backwards, until the array is over
            compare += 1
            if array[place] < value:                                        # If there is a lower value than the selected, stop searching
                break
            array[place + 1] = array[place]                                 # If it isn't smaller, move it one up the array
            assign += 1
            place -= 1                                                      # Move one down the array
        array[place + 1] = value                                            # If stopped searching and moving bigger values up the array, insert the current value
        assign += 1
        
        running = loopHandling([array[place + 1], array[i]], assign, compare)                   # Loophandling (Highlights insertion place and place where the inserted value was (i, so highest sorted value))
        if not running:
            return f"Assigns: {assign} | Comparisons: {compare}"
        pygame.time.Clock().tick(20)                                                            # Framerate
        
    
algorithms = [
    {
        "name": "Selection",
        "action": selectionSort
    },
    {
        "name": "Double selection",
        "action": doubleSelectionSort
    },
    {
        "name": "Insertion",
        "action": insertionSort
    }
]


# VARIABLES


settings_rects = []         # List of rect values for the buttons in settings menu
text_timer = 0              # Timer for displaying temporary toolbar text for the right amount of time
selected_algo = None        # Int value that represents the place of the selected sorting algorithm in the 'algorithms' list
scroll = 0                  # An +/- int value to represent how much the user has scrolled overall in the setting menu (up = +, down = -)
scrolled = 0                # An + int value to represent how many times has a user scrolled in a given frame


# MAIN LOOP


running = True
while running:

    # Get current screen dimensions
    width, height = screen.get_size()
    
    # Update button/hitbox positions
    buttons[4]["rect"] = settings.get_rect(topleft=(width - 39, 7))             # Settings button
    
    # Reset scrolled count
    scrolled = 0
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                           # Exit game if X is pressed
            running = False
        elif event.type == pygame.MOUSEWHEEL and mode == "settings":            # Scrolling in settings menu
            
            if event.y == -1:                                                   # Scrolled downwards
                if height < (settings_rects[-1][1] + 32 - scrolled * 46):       # Check, if the available buttons to choose from DON'T fit in the current screen
                    scroll -= 1                                                 # Scroll down 46 pixels (button + spacing)
                    scrolled += 1
            if event.y == 1:                                                    # Scrolled upwards
                scroll += 1                                                     # Scroll up 46 pixels
                if scroll > 0:                                                  # If it reaches the top row of buttons, don't scroll higher
                    scroll = 0
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:        # Check if lmb is pressed
            
            if mode == "settings" and settings_rects != []:                     # Settings menu, check sorting algorithm selection buttons
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
                            toolbar_text.append(algorithms[selected_algo]["action"](array[0]))
                            text_timer = -20
                            mode = "main"
                            
                    else:                                                       # Otherwise:
                        toolbar_text.append(button["text"])
                        text_timer = 0
                        mode = "main"
                        button["action"]()                                      # Preform button action


    if len(toolbar_text) > 1:                                       # Handle temporary and permanent toolbar texts
        if text_timer > 40:                                         # Show temporary texts for 40 frames
            toolbar_text = [toolbar_text[0]]
        text_timer += 1
        
    if mode == "main":                                              # Pick appropriate permanent toolbar text
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
    pygame.time.Clock().tick(20)        # Framerate

# Quit pygame
pygame.quit() 
