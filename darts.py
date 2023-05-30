import tkinter as tk
import sqlite3

class Games:
    def __init__(self, sets):
        self.sets = sets


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 501
        self.wins = 0

    def update_score(self, score):
        self.score -= score
        


    def get_score(self):
        return self.score

def high_score(score):
        c.execute("INSERT INTO players (highest_score) VALUES (?)", (score))
        conn.commit()
def is_score_allowed(score):
    disallowed_scores = [179, 178, 176, 175, 173, 172, 169, 166, 163]
    return score not in disallowed_scores


def update_scoreboard():
    player1_score_label.config(text=f"{player1.name} Score: {player1.get_score()} | Wins: {player1.wins}")
    player2_score_label.config(text=f"{player2.name} Score: {player2.get_score()} | Wins: {player2.wins}")

def handle_player_turn(player):
    player_score = player.get_score()
    

    try:
        #Checks for the score if player is on a double
        false  = [180]
        false2 = [180,177]
        false3 = [180,177,174]
        false4 = [180,177,174,171]
        false5 = [180,177,174,171,165]
        false6 = [180,177,174,171,165,162]
        false7 = [180,177,174,171,165,162,159]
        
        #Check if score is correct or even possible
        score = int(score_entry.get())
        #Player can't get score of 1
        newscore = player_score - score
        c.execute("INSERT INTO players (name, wins, highest_score) VALUES (?, ?, ?)", (player.name, player.wins, score))
        conn.commit()
        if score < 0 or score > 180:
            error_label.config(text="Invalid score. Please enter a score between 0 and 180.")
            return

        if not is_score_allowed(score):
            error_label.config(text="Invalid score. That number cannot be thrown.")
            return

        if score > player_score:
            error_label.config(text="Invalid score. It exceeds the remaining score.")
            return
        
        if newscore == 1:
            error_label.config(text="Invalid score. The last turn must finish with a double.")
            return
        if player_score <= 180 and score != 0 and score in false:
            error_label.config(text="Invalid score. The last turn must finish with a double.")
            return
        elif player_score <= 177 and score != 0 and score in false2:
            error_label.config(text="Invalid score. The last turn must finish with a double.")
            return
        elif player_score <= 159 and score != 0 and score in false3:
            error_label.config(text="Invalid score. The last turn must finish with a double.")
            return
        elif player_score <= 171 and score != 0 and score in false4:
            error_label.config(text="Invalid score. The last turn must finish with a double.")
            return
        elif player_score <= 165 and score != 0 and score in false5:
            error_label.config(text="Invalid score. The last turn must finish with a double.")
            return
        elif player_score <= 162 and score != 0 and score in false6:
            error_label.config(text="Invalid score. The last turn must finish with a double.")
            return
        elif player_score <= 159 and score != 0 and score in false7:
            error_label.config(text="Invalid score. The last turn must finish with a double.")
            return


        player.update_score(score)
        update_scoreboard()
        
        if player.get_score() == 0:
            player.wins += 1
            if player.wins == amount_of_games.sets:
                
                winner_label.config(text=f"{player.name} wins the game!")
                score_entry.config(state="disabled")
                # Store player data in the database
                print(score)
                c.execute("INSERT INTO players (name, wins, highest_score) VALUES (?, ?, ?)", (player.name, player.wins, score))
                conn.commit()
                return

            error_label.config(text=f"{player.name} wins the set!")
            score_entry.config(state="disabled")

            # Reset the game for the next leg
            player1.score = 501
            player2.score = 501
            update_scoreboard()
            player_turn_label.config(text=f"{player1.name}'s turn")
            score_entry.config(state="normal")
            score_entry.delete(0, tk.END)
            score_entry.focus_set()
            return

        error_label.config(text="")

        score_entry.delete(0, tk.END)  # Clear the input field

        # Switch turns to the next player
        if player == player1:
            player_turn_label.config(text=f"{player2.name}'s turn")
        else:
            player_turn_label.config(text=f"{player1.name}'s turn")

    except ValueError:
        error_label.config(text="Invalid input. Please enter a number.")


def start_game():
    global amount_of_games
    sets = sets_entry.get()

    if sets.isdigit():
        amount_of_games = Games(int(sets))
        player1.score = 501
        player2.score = 501
        player1.wins = 0
        player2.wins = 0

        player1_score_label.config(text=f"{player1.name} Score: {player1.get_score()} | Wins: {player1.wins}")
        player2_score_label.config(text=f"{player2.name} Score: {player2.get_score()} | Wins: {player2.wins}")

        sets_label.config(text=f"Sets: {amount_of_games.sets}")

        sets_entry.pack_forget()

        start_button.pack_forget()

        score_entry.config(state="normal")
        score_entry.delete(0, tk.END)
        score_entry.focus_set()
        player_turn_label.config(text=f"{player1.name}'s turn")
    else:
        error_label.config(text="Invalid input. Please enter integers for sets and legs.")


# Connect to the database
conn = sqlite3.connect('player_data.db')
c = conn.cursor()

# Create players table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS "players" (
	"name"	TEXT,
	"wins"	INTEGER,    
	"highest_score"	TEXT
);''')

# Create the players
player1 = Player("Marco")
player2 = Player("Herman")

# Create the main window
window = tk.Tk()
window.title("Dart Scoreboard")

# Create GUI elements
player_turn_label = tk.Label(window, text=f"{player1.name}'s turn")
player_turn_label.pack()

player1_score_label = tk.Label(window, text=f"{player1.name} Score: {player1.get_score()} | Wins: {player1.wins}")
player1_score_label.pack()

player2_score_label = tk.Label(window, text=f"{player2.name} Score: {player2.get_score()} | Wins: {player2.wins}")
player2_score_label.pack()

sets_label = tk.Label(window, text="Sets:")
sets_label.pack()

sets_entry = tk.Entry(window)
sets_entry.pack()

start_button = tk.Button(window, text="Start Game", command=start_game, background="blue", cursor="")
start_button.pack()

score_entry = tk.Entry(window)
score_entry.pack()

error_label = tk.Label(window, fg="red")
error_label.pack()

submit_button = tk.Button(window, text="Submit",
                          command=lambda: handle_player_turn(player1 if player_turn_label.cget("text") == f"{player1.name}'s turn" else player2))
submit_button.pack()

winner_label = tk.Label(window, fg="blue")
winner_label.pack()

# Start the GUI event loop
window.mainloop()

# Close the database connection
conn.close()
