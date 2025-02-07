import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Kuca")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set font
font = pygame.font.Font(None, 74)

# Create text surface
text = font.render('Kuca', True, BLACK)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill screen with white
    screen.fill(WHITE)
    
    # Draw text in the center
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
