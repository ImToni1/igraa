import pygame
import sys

from abc import ABC, abstractmethod

# Inicijalizacija Pygame-a
pygame.init()

# Postavke ekrana
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Klikni na krug")

# Boje
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Parametri za krugove
circle_radius = 40
circle_labels = []  # Dinamički ćemo dodavati labelu za svaki krug
circle_positions = []  # Koordinate svih krugova
clicked = []  # Status klika za svaki krug
circle_rows = []  # Informacije o redovima krugova

# Apstraktna tvornica za krugove
class CircleFactory(ABC):
    @abstractmethod
    def create_circle(self):
        pass

# Konkretna tvornica za "Povrat kući"
class HomeCircleFactory(CircleFactory):
    def create_circle(self):
        return [("Povrat kući", (300, 50), 1)]  # Povratak kući na vrhu piramide, red 1

# Konkretna tvornica za "Back"
class BackCircleFactory(CircleFactory):
    def create_circle(self):
        return [("Back", (300, 350), 6)]  # Back na dnu piramide, red 6

# Konkretna tvornica za "Nešto drugo"
class RandomCircleFactory(CircleFactory):
    def create_circle(self):
        positions = []
        row_count = 2  # Početni broj krugova u drugom redu
        x_offset = 120  # Pomeranje za pozicije u piramidi
        y_offset = 65  # Razmak između redova
        
        # Dodajemo piramidalno raspoređene krugove
        for row in range(2, 5):  # Red 2 do 5
            for i in range(row_count):
                x_pos = 300 - (row_count - 1) * x_offset / 2 + i * x_offset  # Centriranje u redu
                y_pos = 1 + row * y_offset  # Visina na kojoj se nalazi red
                positions.append(("Nešto drugo", (x_pos, y_pos), row))
            row_count += 1  # Povećaj broj krugova za sljedeći red
        
        return positions

# Funkcija za crtanje krugova
def draw_circles():
    for i, pos in enumerate(circle_positions):
        color = RED if clicked[i] else BLUE
        pygame.draw.circle(screen, color, pos, circle_radius)
        font = pygame.font.Font(None, 24)
        text = font.render(circle_labels[i], True, WHITE)
        text_rect = text.get_rect(center=pos)
        screen.blit(text, text_rect)

# Funkcija za provjeru klika na krug
def check_click(pos):
    for i, circle_pos in enumerate(circle_positions):
        distance = ((pos[0] - circle_pos[0]) ** 2 + (pos[1] - circle_pos[1]) ** 2) ** 0.5
        if distance < circle_radius and not clicked[i]:
            clicked[i] = True
            row = circle_rows[i]  # Dobi red u kojem se nalazi krug
            # Zacrveni cijeli red
            for j, row_value in enumerate(circle_rows):
                if row_value == row:  # Ako je u istom redu
                    clicked[j] = True
            return i  # Vraća indeks kruga koji je kliknut
    return -1  # Ako nijedan krug nije kliknut

# Funkcija za inicijalizaciju tvornica
def initialize_factories():
    home_factory = HomeCircleFactory()
    back_factory = BackCircleFactory()
    random_factory = RandomCircleFactory()

    # Stvaranje krugova pomoću tvornica
    home_circles = home_factory.create_circle()
    back_circles = back_factory.create_circle()
    random_circles = random_factory.create_circle()

    # Kombiniraj sve krugove u jedan popis
    all_circles = home_circles + random_circles + back_circles

    # Ažuriraj globalne liste
    for label, pos, row in all_circles:
        circle_labels.append(label)
        circle_positions.append(pos)
        circle_rows.append(row)  # Spremi red za svaki krug
        clicked.append(False)  # Početno, nijedan krug nije kliknut

# Glavna petlja igre
running = True
initialize_factories()  # Pokreni tvornice i dobij sve krugove

while running:
    screen.fill(WHITE)  # Ispuni ekran bijelom bojom

    # Provjera događaja
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_index = check_click(mouse_pos)
            if clicked_index != -1:
                # Ispis rezultata ovisno o kliknutom krugu
                print(f"Kliknuo si na: {circle_labels[clicked_index]}")  # Ispis naziva kruga

    draw_circles()  # Crtanje svih krugova

    pygame.display.flip()  # Ažuriraj ekran

pygame.quit()
sys.exit()
