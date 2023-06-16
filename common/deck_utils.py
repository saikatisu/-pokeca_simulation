import random
import configparser

class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

def draw_cards(deck, num_cards):
    drawn_cards = random.sample(deck, num_cards)
    remaining_deck = deck.copy()  # デッキのコピーを作成
    for card in drawn_cards:
        remaining_deck.remove(card)  # 取り出したカードをデッキから削除
    return drawn_cards, remaining_deck

def has_seed_pokemon(hand, seed_pokemon):
    return any(card in seed_pokemon for card in hand)

def has_specific_card(hand, target_card):
    return target_card in hand

def initialize_deck(deck_list):
    deck = []
    for card_type, card_dict in deck_list.items():
        for card_name, card_count in card_dict.items():
            deck.extend([card_name] * int(card_count))
    return deck

def generate_random_hand(deck, target_cards, excluded_card=None, num_cards=7):
    hand = []
    
    # 特定カードが含まれている場合にはそのまま手札に追加
    for target_card in target_cards:
        if target_card not in hand:
            hand.append(target_card)
            deck.remove(target_card)
    
    # 残りのカードを引く
    while len(hand) < num_cards:
        draw_card = random.choice(deck)
        
        # 排除カードが指定されている場合、それを含むカードは引かない
        if excluded_card and draw_card == excluded_card:
            continue
        
        hand.append(draw_card)
        deck.remove(draw_card)
    
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

def deck_compression(hand, deck):
    """
	TODO デッキ圧縮処理 手札にグッツがあれば使用する。
	概要 グッツを利用してデッキを圧縮するメソッド
	引数
		hand 手札
		deck デッキ
	return 手札 デッキ
	"""
    # TODO グッツ利用優先度をチェックして、グッツ効果処理をする
    hand, deck = compress_deck_with_level_ball(hand, deck)
    hand, deck = compress_deck_with_mist_crystal(hand, deck)
    hand, deck = compress_deck_with_hyper_ball(hand, deck)
    
	# TODO 手札とデッキの状況を返却する
    return hand,deck

def compress_deck_with_level_ball(hand, deck):
    """
    TODO デッキ圧縮処理 手札にレベルボールがあれば使用する。
    概要 レベルボールを利用してデッキを圧縮するメソッド
    引数
        hand 手札
        deck デッキ
    return 手札 デッキ
    """
    # HP90以下のポケモンを定義
    target_pokemon = ['ラルトス(テレポートブレイク)','ラルトス(メモリースキップ)','キルリア','ミュウ','マナフィ']
    
    if "レベルボール" in hand:
        # レベルボールを手札から全て使うまでループする
        while "レベルボール" in hand:
            # レベルボールを手札から一枚削除する
            hand.remove("レベルボール")
            
            # deckからHP90以下のポケモンの中で要素番号が低いものを優先に一枚選択
            selected_card = None
            for pokemon in target_pokemon:
                if pokemon in deck:
                    selected_card = pokemon
                    break
            
            # 選択したカードをhandに加える
            if selected_card:
                hand.append(selected_card)
                
                # 選択したカードをdeckから削除する
                deck.remove(selected_card)
        
    return hand, deck

def compress_deck_with_mist_crystal(hand, deck):
    """
    TODO デッキ圧縮処理 手札に霧の水晶があれば使用する。
    概要 霧の水晶を利用してデッキを圧縮するメソッド
    引数
        hand 手札
        deck デッキ
    return 手札 デッキ
    """
    # HP90以下のポケモンを定義
    target_card = ['ラルトス(テレポートブレイク)','ラルトス(メモリースキップ)','基本超エネルギー','ミュウ','クレセリア']
    
    if "霧の水晶" in hand:
         while "霧の水晶" in hand:
            # 霧の水晶を手札から一枚削除する
            hand.remove("霧の水晶")
            
            # deckからtarget_cardの中で要素番号が低いものを優先に一枚選択
            selected_card = None
            for pokemon in target_card:
                if pokemon in deck:
                    selected_card = pokemon
                    break
            
            # 選択したカードをhandに加える
            if selected_card:
                hand.append(selected_card)
                
                # 選択したカードをdeckから削除する
                deck.remove(selected_card)
        
    return hand, deck

def compress_deck_with_hyper_ball(hand, deck):
    """
    TODO デッキ圧縮処理 手札にハイパーボールがあれば使用する。
    概要 ハイパーボールを利用してデッキを圧縮するメソッド
    引数
        hand 手札
        deck デッキ
    return 手札 デッキ
    """
    trash_card = ['基本超エネルギー', 'シンオウ神殿', 'ナンジャモ', 'ボスの指令（アカギ）', 'ふしぎなアメ', 'すごいつりざお', 'ともだちてちょう']
    target_pokemon = ['ラルトス(テレポートブレイク)', 'ラルトス(メモリースキップ)', 'かがやくゲッコウガ', 'キルリア', 'ミュウ', 'マナフィ', 'クレセリア', 'サーナイトex', 'サーナイト', 'ザシアンV']
    
    while "ハイパーボール" in hand:
        # トラッシュカードの種類数と同名カードの枚数をカウント
        trash_card_count = len(set(trash_card) & set(hand))
        same_card_count = max(hand.count(card) for card in trash_card)
        
        # ハイパーボールの使用条件を満たしているかチェック
        if trash_card_count >= 2 or same_card_count >= 2:
            # ハイパーボールを手札から一枚削除する
            hand.remove("ハイパーボール")
            
            # deckからtarget_pokemonの中で要素番号が低いものを優先に一枚選択
            selected_card = None
            for pokemon in target_pokemon:
                if pokemon in deck:
                    selected_card = pokemon
                    break
            
            # 選択したカードをhandに加える
            if selected_card:
                hand.append(selected_card)
                
                # 選択したカードをdeckから削除する
                deck.remove(selected_card)
                
                # トラッシュカードに指定されたカードを2枚削除する
                for card in trash_card:
                    for _ in range(2):
                        if card in hand:
                            hand.remove(card)
        else:
            # 使用条件を満たしていない場合はループから抜ける
            break
    
    return hand, deck
