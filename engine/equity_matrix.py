from treys import Card, Evaluator, Deck
from itertools import combinations
from engine.equity_calc import parse_cards
import time

# All ranks high to low for matrix
RANKS = 'AKQJT98765432'

def hand_label(r1, r2, suited):
    if r1 == r2:
        return r1 + r2  # e.g. AA
    return f"{r1}{r2}{'s' if suited else 'o'}"

def generate_equity_matrix(villain_hand_str, board_str):
    villain_hand = parse_cards(villain_hand_str)
    board = parse_cards(board_str)

    # --- Duplicate check ---
    all_cards = villain_hand + board
    if len(set(all_cards)) != len(all_cards):
        raise ValueError("Duplicate cards detected between villain hand and board.")

    used = set(all_cards)

    evaluator = Evaluator()
    deck = Deck()
    matrix = {}

    # Create 13x13 matrix of hands
    for i, r1 in enumerate(RANKS):
        for j, r2 in enumerate(RANKS):
            if i < j:
                suited = True
            elif i > j:
                suited = False
            else:
                suited = None  # pocket pair

            label = hand_label(r1, r2, suited if suited is not None else False)
            total = win = tie = 0
            combos = []

            # Generate combos of this hero hand
            for c1 in [c for c in deck.cards if Card.int_to_str(c)[0] == r1]:
                for c2 in [c for c in deck.cards if Card.int_to_str(c)[0] == r2]:
                    if c1 == c2:
                        continue

                    if c1 in used or c2 in used:
                        continue

                    if suited is None:
                        if Card.get_suit(c1) == Card.get_suit(c2) and r1 == r2:
                            combos.append((c1, c2))
                    elif suited:
                        if Card.get_suit(c1) == Card.get_suit(c2) and r1 != r2:
                            combos.append((c1, c2))
                    else:
                        if Card.get_suit(c1) != Card.get_suit(c2) and r1 != r2:
                            combos.append((c1, c2))

            for hero_hand in combos:
                remaining_deck = [c for c in deck.cards if c not in (used | set(hero_hand))]

                for turn, river in combinations(remaining_deck, 2):
                    full_board = board + [turn, river]
                    hero_score = evaluator.evaluate(full_board, list(hero_hand))
                    villain_score = evaluator.evaluate(full_board, villain_hand)

                    if hero_score < villain_score:
                        win += 1
                    elif hero_score == villain_score:
                        tie += 1

                    total += 1

            matrix[label] = {
                'equity': round((win + tie * 0.5) / total * 100, 2) if total > 0 else 0,
                'combos': len(combos)
            }

    return matrix
