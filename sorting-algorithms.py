# IEatSpaceRocks, 06/09/2026


# SETUP

import pygame, random, os, pygame.freetype              # Libraries
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # Changing the directory to the folder in which the .txt files and main.py are in
pygame.init()                                           # Initialize Pygame

# Create a list and shuffle it
list = [[], []]
for i in range(100):
    list[0].append(i + 1)
random.shuffle(list[0])

# Set up screen
width, height = 800, 800
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Sorting Algorithms")

# Set up text
font = pygame.freetype.Font(None, 30)
text = "Sorting Algorithms"
mode = "main"

# Load images
def loadImage(name):
    return pygame.image.load(f"assets/{name}").convert()
save = loadImage("save.png")
load = loadImage("load.png")
shuffle = loadImage("shuffle.png")
run = loadImage("play.png")
settings = loadImage("settings.png")
exit = loadImage("exit.png")


# Buttons

def saveBtn():
    list[1] = []
    for item in list[0]:
        list[1].append(item)
    return "Saved", "main"
    
def loadBtn():
    if list[1] != []:
        list[0] = []
        for item in list[1]:
            list[0].append(item)
        return "Loaded", "main"
    else:
        return text, mode
        
def shuffleBtn():
    random.shuffle(list[0])
    return "Shuffled", "main"
    
def playBtn():
    list[0].sort()
    
def settingsBtn():
    if mode == "main":
        return "Settings", "settings"
    else:
        return "Sorting Algorithms", "main"


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
        "image": run,
        "rect": run.get_rect(topleft=(124, 7)),
        "action": playBtn,
    },
    {
        "image": settings,
        "rect": settings.get_rect(topleft=(width - 39, 7)),
        "action": settingsBtn,
    },
]


# MAIN LOOP

running = True
while running:
    
    # Get current screen dimensions
    width, height = screen.get_size()
    
    # Update button/hitbox positions
    buttons[4]["rect"] = settings.get_rect(topleft=(width - 39, 7))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # Exit game if X or ESC pressed
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    # Check if any buttons are pressed
            for button in buttons:
                if button["rect"].collidepoint(event.pos):
                    text, mode = button["action"]()                        # Preform button action

    
    # SORTING GOES HERE
    
    # Clear screen
    screen.fill((39, 39, 54))
    
    # Draw toolbar and buttons
    pygame.draw.rect(screen, (112, 128, 144), (0, 0, width, 50))
    pygame.draw.rect(screen, (194, 194, 209), (0, 46, width, 5))
    pygame.draw.rect(screen, (48, 60, 76), (163, 7, width - 209, 32))
    for button in buttons:
        screen.blit(button["image"], button["rect"])
    
    # Draw text
    rect = font.get_rect(text)
    rect.center = ((width - 209) / 2 + 163, 23)
    font.render_to(screen, rect, text, (255, 255, 235))

    if mode == "main":
        # Draw columns
        count = 0
        for col in list[0]:
            pygame.draw.rect(screen, (242, 166, 94), (width / 100 * count, height - (height-51) / 100 * col, width / 100, height))
            count += 1
    
    else:
        # Draw exit button
        screen.blit(exit, exit.get_rect(topleft=(width - 39, 7)))

    # Update screen
    pygame.display.flip()

    # 60 fps
    pygame.time.Clock().tick(6)

pygame.quit() 
