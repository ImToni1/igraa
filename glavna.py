import pygame
import sys


def start_game():
    pygame.init()


    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Lik se okreće kad ide lijevo")


    background_image = pygame.image.load("Slike/Pozadina.png")
    background_width = background_image.get_width()
    character_image = pygame.image.load(selected_player)
    character_image = pygame.transform.scale(character_image, (300, 300))

    x_position = 300    
    y_position = 300      
    speed = 5             
   

    background_x = 0      
    offset_x = 0           
    y_velocity = 0         
    facing_right = True    
    is_blocked = False    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not is_blocked:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                offset_x += speed
                if not facing_right:
                    character_image = pygame.transform.flip(character_image, True, False)
                    facing_right = True
              

            if keys[pygame.K_a]:
                offset_x -= speed
                if facing_right:
                    character_image = pygame.transform.flip(character_image, True, False)
                    facing_right = False


        if   x_position + 300 >  x_position <  + 100:
            is_blocked = True
        else:
            is_blocked = False

        background_x = -(offset_x % background_width)

        screen.blit(background_image, (background_x, 0))  
        screen.blit(background_image, (background_x + background_width, 0))  

        screen.blit(character_image, (x_position, y_position))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    selected_player = sys.argv[1]
    start_game()
