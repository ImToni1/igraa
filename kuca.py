import pygame
import random
import json
import os

pygame.init()

# Postavke ekrana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Swap Game")

# Boje
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Karakteristike karata
CARD_WIDTH, CARD_HEIGHT = 100, 150
CARD_GAP = 20
CARD_Y = HEIGHT - CARD_HEIGHT - 50
POOL_Y = CARD_Y - 200

# Liste za karte
deck = [f"Card {i}" for i in range(1, 21)]  # Dek od 20 karata
hand = []  # Početna ruka je prazna dok ne učitamo karte
pool = random.sample([c for c in deck if c not in hand], 7)  # 7 dostupnih karata
selected_hand_card = None
selected_pool_card = None
swap_mode = False
show_save_message = False
message_timer = 0

# Font
font = pygame.font.Font(None, 36)

def load_hand():
    global hand
    if os.path.exists("saved_hand.json"):
        with open("saved_hand.json", "r") as file:
            try:
                hand = json.load(file)
                # Provjeravamo je li učitana ruka s točno 3 karte
                if len(hand) != 3 or not all(card in deck for card in hand):
                    raise ValueError("Invalid hand in JSON")
            except (json.JSONDecodeError, ValueError):
                # Ako je došlo do greške u čitanju ili formatu, uzimamo nasumične karte
                hand = random.sample(deck, 3)
    else:
        hand = random.sample(deck, 3)

def draw_cards():
    screen.fill(WHITE)
    x = max(0, min((WIDTH - (3 * CARD_WIDTH + 2 * CARD_GAP)) // 2, WIDTH - (3 * CARD_WIDTH + 2 * CARD_GAP)))
    for i, card in enumerate(hand):
        rect = pygame.Rect(x, CARD_Y, CARD_WIDTH, CARD_HEIGHT)
        if selected_hand_card == i:
            rect.inflate_ip(20, 20)  # Povećaj kartu ako je odabrana
        pygame.draw.rect(screen, RED if selected_hand_card == i else BLACK, rect, 3)
        text = font.render(card, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 10))
        x += CARD_WIDTH + CARD_GAP
    
    if swap_mode:
        x = max(0, min((WIDTH - (7 * CARD_WIDTH + 6 * CARD_GAP)) // 2, WIDTH - (7 * CARD_WIDTH + 6 * CARD_GAP)))
        for i, card in enumerate(pool):
            rect = pygame.Rect(x, POOL_Y, CARD_WIDTH, CARD_HEIGHT)
            if selected_pool_card == i:
                rect.inflate_ip(20, 20)  # Povećaj kartu ako je odabrana
            pygame.draw.rect(screen, RED if selected_pool_card == i else BLACK, rect, 3)
            text = font.render(card, True, BLACK)
            screen.blit(text, (rect.x + 10, rect.y + 10))
            x += CARD_WIDTH + CARD_GAP
    
    if show_save_message:
        message = font.render("Karte su spremljene!", True, BLACK)
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2))
    
    pygame.display.flip()

def swap_card():
    global hand, pool, selected_hand_card, selected_pool_card
    if selected_hand_card is not None and selected_pool_card is not None:
        hand[selected_hand_card], pool[selected_pool_card] = pool[selected_pool_card], hand[selected_hand_card]
        selected_hand_card = None
        selected_pool_card = None

def save_hand():
    global show_save_message, message_timer
    with open("saved_hand.json", "w") as file:
        json.dump(hand, file)
    show_save_message = True
    message_timer = pygame.time.get_ticks()
    os.system("python test.py")
    pygame.quit()

def get_card_index(pos, y, count):
    x = max(0, min((WIDTH - (count * CARD_WIDTH + (count - 1) * CARD_GAP)) // 2, WIDTH - (count * CARD_WIDTH + (count - 1) * CARD_GAP)))
    for i in range(count):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if rect.collidepoint(pos):
            return i
        x += CARD_WIDTH + CARD_GAP
    return None

# Učitaj ruku na početku igre
load_hand()

# Glavna petlja igre
running = True
while running:
    draw_cards()
    if show_save_message and pygame.time.get_ticks() - message_timer > 2000:
        show_save_message = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if swap_mode:
                index = get_card_index(event.pos, POOL_Y, 7)
                if index is not None:
                    selected_pool_card = index
                else:
                    index = get_card_index(event.pos, CARD_Y, 3)
                    if index is not None:
                        selected_hand_card = index
                if selected_hand_card is not None and selected_pool_card is not None:
                    swap_card()
            else:
                index = get_card_index(event.pos, CARD_Y, 3)
                if index is not None:
                    selected_hand_card = index
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                swap_mode = not swap_mode
                selected_hand_card = None
                selected_pool_card = None
            elif event.key == pygame.K_s:
                save_hand()

pygame.quit()
