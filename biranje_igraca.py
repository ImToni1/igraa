import pygame
import sys
import os

def select_player_screen():
    pygame.init()
 
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Select Player")
    font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 60)
   
    background = pygame.image.load("Slike/Pozadina.png")  
    bg_x = 0  
    bg_speed = 2  

    players = ["Slike/player1.png", "Slike/player2.png", "Slike/player3.png"]
    player_images = [pygame.image.load(p) for p in players]
    
    player_size = (250, 300) 
    player_images = [pygame.transform.scale(img, player_size) for img in player_images]
    
    selected_player = None
    positions = [(65, 225), (265, 225), (465, 225)] 
    
    running = True
    hovered_index = None  
    while running:
        screen.fill((0, 0, 0))
        
        bg_x -= bg_speed
        if bg_x <= -800:
            bg_x = 0
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + 800, 0)) 
        
        title_text = title_font.render("Odaberi karaktera", True, (255, 255, 255))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 150))
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, img in enumerate(player_images):
            img_rect = pygame.Rect(positions[i][0], positions[i][1], player_size[0], player_size[1])
            if img_rect.collidepoint(mouse_x, mouse_y):
                hovered_index = i
                enlarged_img = pygame.transform.scale(player_images[i], (270, 320))
                screen.blit(enlarged_img, (positions[i][0] - 10, positions[i][1] - 10))
            else:
                screen.blit(img, positions[i])
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, pos in enumerate(positions):
                    img_rect = pygame.Rect(pos[0], pos[1], player_size[0], player_size[1])
                    if img_rect.collidepoint(x, y):
                        selected_player = players[i]
                        print(f"Selected player: {selected_player}")
                        running = False
    
    return selected_player  

if __name__ == "__main__":
    selected = select_player_screen()
    os.system(f"python glavna2.py {selected}")
