import pygame
import sys
import os

def start_screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Start Screen")
    font = pygame.font.Font(None, 50)
    text = font.render("Press ANY key to continue", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 300))
    pygame.mixer.music.load("Slike/music.mp3")  
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    
    background = pygame.image.load("Slike/Pozadina.png")  
    bg_x = 0  
    bg_speed = 2  

    running = True
    while running:
        screen.fill((0, 0, 0))
        bg_x -= bg_speed
        if bg_x <= -800:
            bg_x = 0
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + 800, 0))  
        
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False
                os.system("python biranje_igraca.py")  

    return  
if __name__ == "__main__":
    start_screen()
    pygame.quit()