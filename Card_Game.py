import random

# Define constants
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
POWER = {
    '7': 7, '8': 8, '9': 9, '10': 10,
    'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
}
QUOTAS = {0: 5, 1: 3, 2: 2}  # Dealer's right (5), dealer's left (3), dealer (2)

# Function to initialize deck
def initialize_deck():
    deck = [{'rank': rank, 'suit': suit} for suit in SUITS for rank in RANKS]
    # Remove two sevens to make it a 30-card deck
    deck.remove({'rank': '7', 'suit': 'Diamonds'})
    deck.remove({'rank': '7', 'suit': 'Clubs'})
    return deck

# Function to deal cards to players
def deal_cards(deck):
    random.shuffle(deck)
    hands = [deck[i::3] for i in range(3)]
    return hands

#displaying first 5 cards to player who is selecting the trump
def display_hand_start(player, hand):
    print(f"Player {player + 1}'s Hand:")
    for idx, card in enumerate(hand[:5]):
        print(f"{idx}: {card['rank']} of {card['suit']}")
    print()


# Function to display cards in hand, sorted by suit and rank
def display_hand(player, hand):
    print(f"Player {player + 1}'s Hand:")
    for idx, card in enumerate(hand):
        print(f"{idx}: {card['rank']} of {card['suit']}")
    print()

# Function to play a card
def play_card(player, hand, lead_suit, trump_suit):
    display_hand(player, hand)
    while True:
        try:
            card_index = int(input(f"Player {player + 1}, enter the index of the card to play: "))
            card_played = hand[card_index]

            # Enforce rule about following the lead suit
            if lead_suit and card_played['suit'] != lead_suit:
                if any(card['suit'] == lead_suit for card in hand):
                    raise ValueError(f"You must follow suit and play a {lead_suit} card.\n")
            
            hand.pop(card_index)
            return {'player': player, 'card': card_played}
        except ValueError as ve:
            print(ve)
        except IndexError:
            print("Invalid input. Please enter a valid index.\n")

# Function to determine the winner of a trick
def determine_trick_winner(cards_played, trump_suit, lead_suit):
    winning_card = cards_played[0]['card']
    winning_player = cards_played[0]['player']
    
    for entry in cards_played[1:]:
        card = entry['card']
        
        if card['suit'] == winning_card['suit']:
            if POWER[card['rank']] > POWER[winning_card['rank']]:
                winning_card = card
                winning_player = entry['player']
        elif card['suit'] == trump_suit:
            if winning_card['suit'] != trump_suit or POWER[card['rank']] > POWER[winning_card['rank']]:
                winning_card = card
                winning_player = entry['player']
        elif card['suit'] == lead_suit and winning_card['suit'] != trump_suit:
            if POWER[card['rank']] > POWER[winning_card['rank']]:
                winning_card = card
                winning_player = entry['player']
                
    return winning_player

# Function to check if a player has won
def check_winner(tricks_won):
    return all(tricks_won[player] >= QUOTAS[player] for player in range(3))

# Main function to run the game
def play_game():
    while True:
        deck = initialize_deck()
        hands = deal_cards(deck)
        dealer_index = 2
        trump_suit = None

        print("Dealer is Player 3")
        current_player = (dealer_index + 1) % 3

        # Player to dealer's right chooses the trump suit
        display_hand_start(current_player, hands[current_player])
        while True:
            try:
                trump_choice = int(input(f"Player {current_player + 1}, choose the trump suit (1: Hearts, 2: Diamonds, 3: Clubs, 4: Spades): "))
                if 1 <= trump_choice <= 4:
                    trump_suit = SUITS[trump_choice - 1]
                    break
                else:
                    print("Invalid choice. Please choose a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")
        print(f"Trump suit chosen: {trump_suit}")

        tricks_won = [0, 0, 0]

        # Play 10 tricks
        for trick in range(10):
            print(f"Trick {trick + 1}:")
            cards_played = []
            lead_suit = None
            for _ in range(3):
                card_played = play_card(current_player, hands[current_player], lead_suit, trump_suit)
                if lead_suit is None:
                    lead_suit = card_played['card']['suit']
                cards_played.append(card_played)
                print(f"Player {current_player + 1} played: {card_played['card']['rank']} of {card_played['card']['suit']}")
                current_player = (current_player + 1) % 3

            trick_winner = determine_trick_winner(cards_played, trump_suit, lead_suit)
            tricks_won[trick_winner] += 1
            current_player = trick_winner
            print(f"Player {current_player + 1} wins the trick!\n")

            # Display the score after each trick
            print(f"Scores: Player 1: {tricks_won[0]}, Player 2: {tricks_won[1]}, Player 3: {tricks_won[2]}\n")

        print("Game Over!")
        for player in range(3):
            print(f"Player {player + 1} won {tricks_won[player]} tricks (Quota: {QUOTAS[player]})")

        if check_winner(tricks_won):
            print("All players met their quotas. It's a tie!")

        else:
            for player in range(3):
                if tricks_won[player] >= QUOTAS[player]:
                    print(f"Player {player + 1} has met their quota and wins.")
                else:
                    print(f"Player {player + 1} did not meet their quota and loses.")

        # Ask if the players want to play again
        play_again = input("Press 1 to play again or 2 to quit: ").strip()
        if play_again != '1':
            print("Thanks for playing the game!!")
            break  # Exit the loop and end the game

# Run the game
if __name__ == "__main__":
    play_game()
