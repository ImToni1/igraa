import pygame
import sys
import time
import os

def load_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

def game_loop():
    pygame.init()
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Kuća i Portal")
    
    background_image = load_image("Slike/Pozadina.png", (800, 600))
    character_image = pygame.image.load(selected_player)
    character_image = pygame.transform.scale(character_image, (300, 300))
    house_image = load_image("Slike/home.jpg", (120, 120))
    portal_image = load_image("Slike/portal.png", (120, 120))
 
    
    clock = pygame.time.Clock()
    
    x_position = 300
    y_position = 270
    speed = 5
    facing_right = True
    last_interaction_time = 0
    cooldown = 2  # Sekunde
    
    house_rect = pygame.Rect(50, 420, 120, 120)
    portal_rect = pygame.Rect(630, 420, 120, 120)
    character_rect = pygame.Rect(x_position, y_position, 180, 180)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            x_position += speed
            if not facing_right:
                character_image = pygame.transform.flip(character_image, True, False)
                facing_right = True
        elif keys[pygame.K_a]:
            x_position -= speed
            if facing_right:
                character_image = pygame.transform.flip(character_image, True, False)
                facing_right = False
        
        character_rect.x = x_position
        
        current_time = time.time()
        if keys[pygame.K_e] and (current_time - last_interaction_time >= cooldown):
            if character_rect.colliderect(house_rect):
                print("Usao si u kuću! Prelazak na drugi ekran...")
                os.system("python kuca.py")
                last_interaction_time = current_time
            elif character_rect.colliderect(portal_rect):
                print("Usao si u portal! Prelazak na drugi ekran...")
                os.system("python portal.py")
                last_interaction_time = current_time
        
        screen.blit(background_image, (0, 0))
        screen.blit(house_image, (house_rect.x, house_rect.y))
        screen.blit(portal_image, (portal_rect.x, portal_rect.y))
        screen.blit(character_image, (x_position, y_position))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    selected_player = sys.argv[1]
    game_loop()
    