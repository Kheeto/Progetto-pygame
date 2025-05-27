import pygame
import random
from collections import deque
from core.gamemanager import GameManager

WIDTH, HEIGHT = 1187, 737+50
CARD_WIDTH, CARD_HEIGHT = 90, 135
FPS = 60
CARD_GAP = 10
HOVER_SCALE = 1.1
HAND_X = WIDTH / 2 - 2 * (CARD_WIDTH + CARD_GAP * 0.75)
HAND_Y = HEIGHT - CARD_HEIGHT

MAX_MANA = 10.0
mana = 0.0

CARD_COUNT = 4

card_images = [pygame.image.load(f"src\img\cards\card_{i}.jpg") for i in range(CARD_COUNT)]
card_images = [pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT)) for img in card_images]

mana_costs = {
    0: 3, # dwarven cannon
    1: 2, # elven archer
    2: 4, # goblins
    3: 3, # arcane blast
    4: 5, # troll
    5: 4, # warrior
    6: 6, # balloon
    7: 7} # skeletal knight

font = None

class Card:
    def __init__(self, card_id, pos):
        self.card_id = card_id
        self.image = card_images[card_id]
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.startX = pos[0]
        self.dragging = False
        self.hovered = False

    def draw(self, surface):
        global font
        if font is None:
            font = pygame.font.SysFont(None, 24)

        img = self.image
        if self.hovered:
            img = pygame.transform.scale(self.image, (int(CARD_WIDTH * HOVER_SCALE), int(CARD_HEIGHT * HOVER_SCALE)))
            rect = img.get_rect(center=self.rect.center)
            surface.blit(img, rect)
        else:
            rect = self.rect
            surface.blit(self.image, rect)

        mana_text = font.render(str(mana_costs[self.card_id]), True, (255, 255, 255))
        mana_bg = pygame.Surface((24, 24))
        mana_bg.fill((0, 0, 0))
        mana_bg.blit(mana_text, (4, 4))
        surface.blit(mana_bg, (rect.left + 5, rect.top + 5))

    def update_pos(self, pos):
        self.rect.topleft = pos
        self.pos = pos

def generate_hand(deck, hand_size):
    return random.sample(deck, hand_size)

def get_new_card(deck, hand_ids):
    while deck:
        card_id = deck.popleft()
        if card_id not in hand_ids:
            return card_id
        else:
            deck.append(card_id)
    return None

deck = deque(range(CARD_COUNT))
random.shuffle(deck)

hand = []
for i in range(4):
    x = HAND_X + i * (CARD_WIDTH + CARD_GAP)
    hand.append(Card(deck[i], (x, HAND_Y)))

dragged_card = None
offset_x = 0
offset_y = 0

def Update(screen, events, dt):
    global dragged_card, offset_x, offset_y, mana

    mana = min(mana + dt, MAX_MANA)

    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in hand:
                if card.rect.collidepoint(mouse_pos):
                    dragged_card = card
                    card.dragging = True
                    offset_x = card.rect.x - mouse_pos[0]
                    offset_y = card.rect.y - mouse_pos[1]
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragged_card:
                dragged_card.dragging = False
                # Using a deque for the deck gives more variability but is predictable
                if mouse_pos[1] < HAND_Y and mana_costs[dragged_card.card_id] <= mana:
                    mana -= mana_costs[dragged_card.card_id]
                    GameManager.instance.DeployCard(dragged_card.card_id, mouse_pos)
                    # current_ids = [c.card_id for c in hand]
                    # new_id = get_new_card(deck, current_ids)
                    # if new_id is not None:
                    #     hand.remove(dragged_card)
                    #     hand.append(Card(new_id, (dragged_card.startX, HAND_Y)))
                    # deck.append(dragged_card.card_id)

                dragged_card.update_pos((dragged_card.startX, HAND_Y))
                dragged_card = None

    for card in hand:
        card.hovered = card.rect.collidepoint(mouse_pos)

    if dragged_card is not None and dragged_card.dragging:
        dragged_card.update_pos((mouse_pos[0] + offset_x, mouse_pos[1] + offset_y))

    for card in hand:
        card.draw(screen)
    
    # Mana bar
    bar_width = 400
    bar_height = 20
    bar_x = WIDTH // 2 - bar_width // 2
    bar_y = HEIGHT - 20

    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))  # background
    fill_width = int((mana / MAX_MANA) * bar_width)
    pygame.draw.rect(screen, (0, 0, 255), (bar_x, bar_y, fill_width, bar_height))  # mana fill

    mana_text = font.render(f"{mana:.0f}/{MAX_MANA:.0f}", True, (255, 255, 255))
    screen.blit(mana_text, (bar_x + bar_width + 10, bar_y - 2))