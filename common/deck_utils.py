import random

def draw_cards(deck, num_cards):
    drawn_cards = random.sample(deck, num_cards)
    remaining_deck = deck[:]  # デッキのコピーを作成
    for card in drawn_cards:
        remaining_deck.remove(card)  # 取り出したカードをデッキから削除
    return drawn_cards, remaining_deck

def has_seed_pokemon(hand, seed_pokemon):
    for card in hand:
        if card in seed_pokemon:
            return True
    return False

def has_specific_card(hand, target_card):
    return target_card in hand

def initialize_deck(deck_list):
    deck = []
    for card_type, card_dict in deck_list.items():
        for card_name, card_count in card_dict.items():
            deck.extend([card_name] * int(card_count))
    return deck

