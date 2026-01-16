import pygame
import sys
import random

pygame.init()

# -----------------------------
# Screen setup
# -----------------------------
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solitaire")
clock = pygame.time.Clock()
FPS = 60

# -----------------------------
# Colors
# -----------------------------
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# -----------------------------
# Card class
# -----------------------------
class Card:
    def __init__(self, suit, rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.face_up = face_up
        self.width = 80
        self.height = 120
        self.x = 0
        self.y = 0

    @property
    def color(self):
        return RED if self.suit in ["H", "D"] else BLACK

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, WHITE if self.face_up else BLUE, rect)
        pygame.draw.rect(surface, BLACK, rect, 2)  # border
        if self.face_up:
            font = pygame.font.SysFont(None, 24)
            text = font.render(f"{self.rank}{self.suit}", True, self.color)
            surface.blit(text, (self.x + 5, self.y + 5))

    def is_hovered(self, mouse_pos):
        mx, my = mouse_pos
        return (
            self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height
        )


# -----------------------------
# Deck setup
# -----------------------------
suits = ["S", "H", "D", "C"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = [Card(s, r) for s in suits for r in ranks]
random.shuffle(deck)

# -----------------------------
# Tableau (7 piles)
# -----------------------------
tableau = [[] for _ in range(7)]
for i in range(7):
    for j in range(i + 1):
        card = deck.pop()
        card.face_up = j == i
        tableau[i].append(card)

# -----------------------------
# Stock and Waste piles
# -----------------------------
stock = deck  # remaining cards
waste = []

# -----------------------------
# Foundations
# -----------------------------
foundations = {s: [] for s in suits}


# -----------------------------
# Positions
# -----------------------------
def update_positions():
    # Tableau positions
    start_x = 50
    start_y = 200
    spacing_x = 100
    spacing_y = 30
    for col_index, col in enumerate(tableau):
        for row_index, card in enumerate(col):
            card.x = start_x + col_index * spacing_x
            card.y = start_y + row_index * spacing_y
    # Stock & Waste
    for i, card in enumerate(stock):
        card.x = 50
        card.y = 50
    for i, card in enumerate(waste[-1:]):  # only top waste card
        card.x = 150
        card.y = 50
    # Foundations
    for idx, suit in enumerate(suits):
        if foundations[suit]:
            foundations[suit][-1].x = 400 + idx * 100
            foundations[suit][-1].y = 50


update_positions()

# -----------------------------
# Dragging logic
# -----------------------------
dragging_card = None
drag_offset_x = 0
drag_offset_y = 0
dragging_stack = []
drag_origin_col = None


def get_stack_under_mouse(mouse_pos):
    # Check tableau columns from top to bottom
    for col in tableau:
        for i, card in enumerate(col):
            if card.is_hovered(mouse_pos) and card.face_up:
                # Return the card and all cards below it in the column
                return col[i:]
    # Check waste
    if waste and waste[-1].is_hovered(mouse_pos):
        return [waste[-1]]
    return []


# -----------------------------
# Move validation
# -----------------------------
def can_move_to_tableau(card, target_col):
    if not target_col:
        return card.rank == "K"  # empty column: only King
    top_card = target_col[-1]
    if not top_card.face_up:
        return False
    # alternating colors
    if card.color == top_card.color:
        return False
    # descending rank
    rank_order = {r: i for i, r in enumerate(ranks, 1)}
    return rank_order[card.rank] == rank_order[top_card.rank] - 1


def can_move_to_foundation(card):
    foundation = foundations[card.suit]
    rank_order = {r: i for i, r in enumerate(ranks, 1)}
    if not foundation:
        return card.rank == "A"
    top_card = foundation[-1]
    return rank_order[card.rank] == rank_order[top_card.rank] + 1


# -----------------------------
# Game loop
# -----------------------------
running = True
while running:
    screen.fill(GREEN)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Picking up a stack
            for col in tableau:
                for i, card in enumerate(col):
                    if card.is_hovered(mouse_pos) and card.face_up:
                        dragging_stack = col[i:]  # all cards from this down
                        drag_origin_col = col
                        # Store offset relative to the first card clicked
                        drag_offset_x = mouse_pos[0] - dragging_stack[0].x
                        drag_offset_y = mouse_pos[1] - dragging_stack[0].y
                        break
                if dragging_stack:
                    break
            if not dragging_stack and waste and waste[-1].is_hovered(mouse_pos):
                dragging_stack = [waste[-1]]
                drag_origin_col = None
                drag_offset_x = mouse_pos[0] - dragging_stack[0].x
                drag_offset_y = mouse_pos[1] - dragging_stack[0].y

        # On MOUSEBUTTONUP (left release)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging_stack:
                moved = False
                # Try moving to tableau
                for col in tableau:
                    if col != dragging_stack and can_move_to_tableau(
                        dragging_stack[0], col
                    ):
                        # Remove stack from old column
                        for pile in tableau:
                            for card in dragging_stack:
                                if card in pile:
                                    pile.remove(card)
                        if dragging_stack[0] in waste:
                            waste.remove(dragging_stack[0])
                        # Add stack to new column
                        col.extend(dragging_stack)
                        moved = True
                        break
                # Try moving top card to foundation if single card
                if len(dragging_stack) == 1 and can_move_to_foundation(
                    dragging_stack[0]
                ):
                    card = dragging_stack[0]
                    for pile in tableau:
                        if card in pile:
                            pile.remove(card)
                    if card in waste:
                        waste.remove(card)
                    foundations[card.suit].append(card)
                    moved = True

                dragging_stack = []
                update_positions()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # Right click: draw from stock
            if stock:
                card = stock.pop()
                card.face_up = True
                waste.append(card)
                update_positions()

    # Drag card with mouse
    # Update positions while dragging
    if dragging_stack:
        for i, card in enumerate(dragging_stack):
            card.x = mouse_pos[0] - drag_offset_x
            card.y = (
                mouse_pos[1] - drag_offset_y + i * 30
            )  # spacing between cards in stack

    # -----------------------------
    # Draw everything
    # -----------------------------

    # Draw stock (empty or top card)
    if stock:
        pygame.draw.rect(screen, BLUE, (50, 50, 80, 120))
        pygame.draw.rect(screen, BLACK, (50, 50, 80, 120), 2)
    # Draw waste top card
    for card in waste[-1:]:
        card.draw(screen)

    # Draw foundations (persistent borders + suit hints)
    for idx, suit in enumerate(suits):
        x = 400 + idx * 100
        y = 50
        width, height = 80, 120
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, YELLOW, rect, 2)  # always visible border
        if foundations[suit]:
            foundations[suit][-1].draw(screen)
        else:
            font = pygame.font.SysFont(None, 48)
            text = font.render(suit, True, WHITE)
            screen.blit(text, (x + 25, y + 40))

    # Draw tableau
    for col in tableau:
        for card in col:
            if card != dragging_card:  # draw dragged card on top later
                card.draw(screen)

    # Draw dragged card on top
    if dragging_card:
        dragging_card.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
