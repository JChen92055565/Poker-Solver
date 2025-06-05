# utils/card_utils.py

VALID_RANKS = "23456789TJQKA"
VALID_SUITS = "cdhs"  # clubs, diamonds, hearts, spades

def parse_board_string(board_str):
    board_str = board_str.strip()
    
    if len(board_str) % 2 != 0:
        raise ValueError("Board string must contain complete cards (2 characters each).")

    num_cards = len(board_str) // 2
    if num_cards != 3:
        raise ValueError("Start with a flop, exactly 3 cards must be entered.")

    cards = []
    seen = set()

    for i in range(0, len(board_str), 2):
        rank = board_str[i].upper()
        suit = board_str[i + 1].lower()

        if rank not in VALID_RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in VALID_SUITS:
            raise ValueError(f"Invalid suit: {suit}")

        card = rank + suit
        if card in seen:
            raise ValueError(f"Duplicate card: {card}")
        seen.add(card)
        cards.append((rank, suit))

    return cards
