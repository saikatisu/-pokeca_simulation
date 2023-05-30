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

# deck_utils.py

import random

def generate_random_hand(deck, target_card, excluded_card=None, num_cards=7):
    hand = []
    
    # 特定カードが含まれている場合にはそのまま手札に追加
    if target_card not in hand:
        hand.append(target_card)
        deck.remove(target_card)
    
    # 残りのカードを引く
    while len(hand) < num_cards:
        draw_card = random.sample(deck, 1)[0]
        
        # 排除カードが指定されている場合、それを含むカードは引かない
        if excluded_card and draw_card == excluded_card:
            continue
        
        hand.append(draw_card)
        deck.remove(draw_card)
    
    if len(deck) != 53:
        raise ValueError("デッキ枚数が53枚ではありません")
    
    return hand, deck

def draw_cards_except(deck, num_cards, excluded_cards):
    drawn_cards = []
    
    while len(drawn_cards) < num_cards:
        draw_card = random.choice(deck)
        
        # 排除カードが指定されている場合、それを含むカードは引かない
        if draw_card not in excluded_cards:
            drawn_cards.append(draw_card)
            deck.remove(draw_card)
    
    return drawn_cards, deck



