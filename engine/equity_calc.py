from treys import Card

def parse_cards(card_strs):
    """
    Converts a list of card strings like ['Ah', 'Ks'] into treys integer card representations.
    """
    return [Card.new(c) for c in card_strs]