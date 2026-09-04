# IEatSpaceRocks, 04/09/2026

# SETUP
import pygame, random, os                               # Libraries
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # Changing the directory to the folder in which the .txt files and main.py are in
pygame.init()                                           # Initialize Pygame

# Create a list and shuffle it
list = []
for i in range(100):
    list.append(i + 1)
random.shuffle(list)

# Set up screen
width, height = 800, 800
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Sorting Algorithms")

# Load images
def loadImage(name):
    return pygame.image.load(name).convert()
save = loadImage("assets/save.png")
load = loadImage("assets/load.png")
shuffle = loadImage("assets/shuffle.png")
play = loadImage("assets/play.png")
settings = loadImage("assets/settings.png")

# Set up buttons
buttons = [
    {
        "image": save,
        "rect": save.get_rect(topleft=(7, 7)),
        "action": "Save",
    },
    {
        "image": load,
        "rect": load.get_rect(topleft=(46, 7)),
        "action": "Load",
    },
    {
        "image": shuffle,
        "rect": shuffle.get_rect(topleft=(85, 7)),
        "action": "Shuffle",
    },
    {
        "image": play,
        "rect": play.get_rect(topleft=(124, 7)),
        "action": "Play",
    },
    {
        "image": settings,
        "rect": settings.get_rect(topleft=(width - 39, 7)),
        "action": "Settings",
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
                    print(button["action"])                         # Preform button action
    
    # SORTING GOES HERE
    
    # Clear screen
    screen.fill((7, 12, 16))
    
    # Draw next frame
    pygame.draw.rect(screen, (112, 128, 144), (0, 0, width, 50))
    pygame.draw.rect(screen, (30, 51, 68), (0, 46, width, 4))
    for button in buttons:
        screen.blit(button["image"], button["rect"])
    
    # Draw columns
    count = 0
    for col in list:
        pygame.draw.rect(screen, (255, 255, 255), (width / 100 * count, height - (height-51) / 100 * col, width / 100, height))
        count += 1

    # Update screen
    pygame.display.flip()

    # 60 fps
    pygame.time.Clock().tick(6)

pygame.quit() 
