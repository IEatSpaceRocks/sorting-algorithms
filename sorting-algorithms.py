# IEatSpaceRocks, 03/09/2026

# Libraries
import pygame, random, os

# Changing the directory to the folder in which the .txt files and main.py are in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()

# Create a list and shuffle it
list = []
for i in range(100):
    list.append(i + 1)
# random.shuffle(list)

# Set up screen
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
pygame.display.set_caption("Sorting")

save = pygame.image.load('save.png').convert()

# MAIN LOOP

running = True
while running:
    
    # Get current screen dimensions
    width, height = screen.get_size()
    
    # Exit game if X or ESC pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # SORTING GOES HERE
    
    # Clear screen
    screen.fill((7, 12, 16))
    
    pygame.draw.rect(screen, (112, 128, 144), (0, 0, width, 50))
    pygame.draw.rect(screen, (30, 51, 68), (0, 46, width, 4))
    screen.blit(save, (7, 7))
    
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
                    