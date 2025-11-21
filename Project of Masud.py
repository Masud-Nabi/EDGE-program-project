import random
import time


class VocabularyMatrixGame:
    def __init__(self):
        # 3x3 Matrix initialized with placeholders
        self.matrix = [['_' for _ in range(3)] for _ in range(3)]
        self.filled_cells = 0
        self.total_turns_played = 0
        self.max_turns = 27  # The game ends strictly at 27 inputs

        # Player Database
        self.players = {
            1: {'name': "Player 1", 'mark': 'P1', 'cells': 0, 'time': 0.0},
            2: {'name': "Player 2", 'mark': 'P2', 'cells': 0, 'time': 0.0}
        }
        self.current_player_id = 1

        # Loading 500 Common/Day-to-Day words
        # (Generated list of standard conventional vocabulary)
        self.vocab_library = self.load_conventional_vocab()

    def load_conventional_vocab(self):
        """
        Returns a list of common English words filtered for 4-7 characters.
        """
        # A raw string of conventional words
        raw_text = """
        time year people thing woman life child world school state family student group country problem
        hand part place case week company system program question work number night point home water 
        room mother area money story fact month right study book business issue side kind head house 
        service friend father power hour game line member city community name team minute idea body 
        information back parent face level office door health person history party result change 
        morning reason research girl food moment teacher force education foot policy process study
        offer music river plant garden police crime court human market death price class nature
        photo paper space voice earth table drive break lunch ready visit share happy angry clean
        early learn start round shoes dress phone watch beach field light sound dream focus skill
        value event model matter radio color movie horse birds sugar bread fruit juice chair train
        plane travel guide hotel spend enjoy relax smile laugh cry shout quiet loud quick slow
        dirty sweet fresh spicy salty heavy light thick thin soft hard rough smooth sharp dull
        north south east west wind rain storm snow cloud heat cold cool warm dry wet bank card
        cash coin sale shop store buy sell rent pay cost save rich poor busy free safe risk
        lock keys open shut push pull walk run jump swim fly ride drive stop wait stay live
        love hate like hope wish want need feel think know guess mind care help look hear
        talk speak tell say ask answer reply write read sign draw paint cook bake boil fry
        wash wipe dust sweep iron fold wear size fit tight loose short long tall high low
        deep wide narrow near far here there where when what which who why how much many
        full empty half whole part some none all both each every other another same real
        true false wrong right good bad best worse fine nice okay sure maybe perhaps yes
        """
        # Process: Split, strip, lowercase, and filter length (4 to 7 chars)
        words = [w.strip().lower() for w in raw_text.split()]
        filtered_words = [w for w in words if 4 <= len(w) <= 7]

        # Ensure we have enough unique words
        unique_words = list(set(filtered_words))
        return unique_words

    def get_word_by_difficulty(self):
        """
        Increases word length based on how many cells are filled.
        """
        # Difficulty Logic:
        # 0-2 cells filled: Length 4-5
        # 3-5 cells filled: Length 5-6
        # 6-8 cells filled: Length 6-7

        if self.filled_cells < 3:
            target_lens = [4, 5]
        elif self.filled_cells < 6:
            target_lens = [5, 6]
        else:
            target_lens = [6, 7]

        candidates = [w for w in self.vocab_library if len(w) in target_lens]

        # Fallback if list is empty (rare)
        if not candidates:
            return random.choice(self.vocab_library)
        return random.choice(candidates)

    def shuffle_word(self, word):
        chars = list(word)
        random.shuffle(chars)
        # Try to ensure it's scrambled
        if "".join(chars) == word:
            random.shuffle(chars)
        return "".join(chars)

    def print_status(self):
        print(f"\n=== MATRIX (Filled: {self.filled_cells}/9) ===")
        print(f"=== TURNS PLAYED: {self.total_turns_played}/{self.max_turns} ===")
        print("-------------------")
        for row in self.matrix:
            print(f"| {row[0]:^4} | {row[1]:^4} | {row[2]:^4} |")
        print("-------------------")

    def update_matrix(self, mark):
        # Auto-fill logic: row = count // 3, col = count % 3
        row = self.filled_cells // 3
        col = self.filled_cells % 3
        self.matrix[row][col] = mark
        self.filled_cells += 1

    def play_turn(self):
        player = self.players[self.current_player_id]

        # 1. Setup Word
        target_word = self.get_word_by_difficulty()
        scrambled = self.shuffle_word(target_word)

        print(f"\n>>> {player['name']}'s Turn")
        print("WARNING: Timer starts immediately with the prompt below!")
        time.sleep(1.5)  # Short pause for readiness

        # 2. Automatic Timer Start
        start_time = time.time()

        # The input prompt shows the scrambled word
        user_input = input(f"Unscramble [ {scrambled} ] >> ").strip().lower()

        end_time = time.time()

        # 3. Update Stats
        duration = end_time - start_time
        player['time'] += duration
        self.total_turns_played += 1

        print(f"   Time Taken: {duration:.2f}s")

        # 4. Validation
        if user_input == target_word:
            if self.filled_cells < 9:
                print(f"   CORRECT! '{target_word}' -> You win a cell.")
                player['cells'] += 1
                self.update_matrix(player['mark'])
            else:
                print(f"   CORRECT! '{target_word}' -> (Matrix full, no cell added)")
        else:
            print(f"   WRONG! The word was '{target_word}'. You lost the strike.")

    def calculate_winner(self):
        print("\n\n###########################################")
        print("              GAME OVER                    ")
        print("###########################################")
        self.print_status()

        highest_score = -999999.0
        winner = "DRAW"

        for pid, p in self.players.items():
            # SCORING FORMULA:
            # 1. Matrix Point = cells * 10
            # 2. Penalty = sum_of_seconds / 50
            # 3. Final = Matrix Point - Penalty

            matrix_points = p['cells'] * 10
            time_penalty = p['time'] / 50
            final_score = matrix_points - time_penalty

            print(f"--- {p['name']} ---")
            print(f" > Cells Won: {p['cells']} (Score: {matrix_points})")
            print(f" > Total Time: {p['time']:.2f}s")
            print(f" > Penalty calculation: {p['time']:.2f} / 50 = -{time_penalty:.4f}")
            print(f" > FINAL SCORE: {final_score:.4f}")
            print("-" * 30)

            if final_score > highest_score:
                highest_score = final_score
                winner = p['name']
            elif final_score == highest_score:
                winner = "DRAW"

        print(f"\n🏆 THE WINNER IS: {winner} 🏆")

    def start(self):
        print("Welcome to the Vocabulary Matrix Quiz!")
        print(f"Goal: Unscramble words (4-7 chars).")
        print(f"Game ends at {self.max_turns} total turns or when matrix fills.")

        # Main Loop
        while self.total_turns_played < self.max_turns and self.filled_cells < 9:
            self.print_status()
            self.play_turn()

            # Switch Player
            self.current_player_id = 2 if self.current_player_id == 1 else 1

        print("\nReason for ending:")
        if self.total_turns_played >= self.max_turns:
            print(f"-> Turn limit ({self.max_turns}) reached.")
        if self.filled_cells >= 9:
            print("-> Matrix is full.")

        self.calculate_winner()


# --- Execution ---
if __name__ == "__main__":
    game = VocabularyMatrixGame()
    game.start()