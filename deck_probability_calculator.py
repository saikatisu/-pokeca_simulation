import os
import common.deck_utils as deck_utils

# デッキの定義をconfig.iniから読み込む
config_file = os.path.join("config", "config.ini")
config = deck_utils.CaseSensitiveConfigParser()
config.read(config_file)

deckList = {}
sections = ['ポケモン', 'グッズ', 'サポート', 'スタジアム', 'エネルギー']

for section in sections:
    if section in config:
        deckList[section] = dict(config[section])

seed_pokemon = config.get('SeedPokemon', 'pokemon', fallback='').split('\n')
target_card = config.get('TargetCard', 'card', fallback='')
initial_hand = config.get("InitialHand", "hand", fallback="").split(", ")


def simulate_probability():
    trials = 1000000  # シミュレーションの試行回数
    success = 0  # 成功回数（目的条件が達成した回数）

    for _ in range(trials):
        deck = deck_utils.initialize_deck(deckList)  # デッキを初期化
        hand, deck = deck_utils.generate_random_hand(deck, initial_hand,target_card) # 固定手札を生成
        
        if len(deck) != 53:
            raise ValueError("デッキ枚数が53枚ではありません")

        while len(hand) < 8:
            if deck_utils.has_seed_pokemon(hand, seed_pokemon):
                side, deck = deck_utils.draw_cards(deck, 6)  # サイドカードとして6枚引く
                
                draw_card, deck = deck_utils.draw_cards_except(deck, 1 ,target_card)  # 山札から1枚引く
                
                hand.append(draw_card[0])
                
                if target_card in hand:
                    raise ValueError("手札生成に誤りがあります")
                    
                else:
                    # 手札圧縮処理
                    hand, deck = deck_utils.deck_compression(hand, deck)
                    
                    # target_cardが手札に存在しない場合は特性「ふしぎなしっぽ」の処理を行う
                    skil_card, deck = deck_utils.draw_cards(deck, 6)  # ふしぎなしっぽの効果で6枚引く
                    
                    if deck_utils.has_specific_card(skil_card, target_card):
                        success += 1
                    break
            else:
                # マリガン処理（試行回数は増やさない）
                deck.extend(hand)  # 手札を山札に戻す
                if len(deck) != 60:
                    raise ValueError("デッキ枚数が60枚ではありません")
                hand, deck = deck_utils.draw_cards(deck, 7)  # 手札を7枚引く

    probability = success / trials
    return probability

probability = simulate_probability()
print("特性「ふしぎなしっぽ」で{}が引ける確率: {:.2%}".format(target_card, probability))