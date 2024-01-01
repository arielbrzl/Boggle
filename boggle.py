import tkinter as tk
import boggle_board_randomizer as h
import datetime
from functools import partial
import ex12_utils as helper

BOARD_SIZE = 4
INIT_SCORE = 0

INITIAL_SECS_LEFT = 3*60
BUTTON_STYLE = {"font": ("courier", 30), "borderwidth": 1}

def read_wordlist(filename):
    """
    returns a list of words read from the given word file
    """
    word_list = []
    f_words = open(filename)
    for line in f_words:
        word = line.strip()
        word_list.append(word)
    f_words.close()
    return word_list


WORDS_LIST = read_wordlist("boggle_dict.txt")


class Score:
    """
    the lowest class in the game's hierarchy, used by the board,
     to define each round's score
    """
    def __init__(self):
        self.score = INIT_SCORE

    def update_score(self, add_score):
        self.score += add_score

    def get_score(self):
        return str(self.score)


class Board:
    """
    each time the user plays a new round of the game,
    the GUI creates a new object of class Board
    """
    def __init__(self):
        self.board = h.randomize_board()
        self.board_dict = self.board_dict_creator()
        self.score = Score()

    def board_dict_creator(self):
        """
        creates a dict:
            key = int from 0 -15
            value - the letter(s) in this position
        :return: the dictionary
        """
        board_dict = {}
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                board_dict[i * BOARD_SIZE + j] = self.board[i][j]

        return board_dict


class MyGui:
    """
    this class defines the general window for the entire game,
    including two frames, as explained in the README file
    """
    def __init__(self, root, board):
        """
        defining ALL the frames, buttons, labels in the game.
        """
        root.title("Boggle")
        self.root = root
        self._main_middle_frame = tk.Frame(self.root, bg="pink", )
        self._main_middle_frame.pack(side="left", expand="true")
        self.word_displayer = tk.Button(self._main_middle_frame,
                                        bg="aquamarine",
                                        height=5, font=("courier", 15),
                                        state="disable",
                                        disabledforeground="black")
        self.word_displayer.pack(side="top", fill="both")
        self.check_word = tk.Button(self._main_middle_frame, text="Check word",
                                    bg="blue violet", height=3,
                                    font=("courier", 15),
                                    command=self.check_word_func)
        self.check_word.pack(side="top", fill="both")
        self.middle_frame_button_frame = tk.Frame(self._main_middle_frame,
                                                  bg="pink")
        self.middle_frame_button_frame.pack(side="top")
        self._buttons = []
        for i in range(BOARD_SIZE * BOARD_SIZE):
            b = tk.Button(self.middle_frame_button_frame,
                          width=3, height=1, font=("Courier", 40))
            b.grid(row=i // BOARD_SIZE,
                   column=i % BOARD_SIZE, )
            self._buttons.append(b)
        self._click_me = tk.Button(self._main_middle_frame, width=20,
                                   height=3, text="Click here to begin!",
                                   font=("courier", 30),
                                   command=self.timer_clicked,
                                   bg="blue violet")
        self._click_me.pack(side="top")
        self.board = board
        self._main_right_frame = tk.Frame(self.root, bg="goldenrod2")
        self._main_right_frame.columnconfigure(0, weight=1)
        self._main_right_frame.pack(side="left", expand=True, fill="both")
        self.correct_words_displayer = tk.Label(self._main_right_frame,
                                                bg="medium purple",
                                                text="Correct words:" + "\n",
                                                anchor="n",
                                                font=("courier", 12),
                                                height=30, width=35)
        self.correct_words_displayer.grid(row=0, column=0, columnspan=20,
                                          sticky="n")
        self._score_displayer = tk.Label(self._main_right_frame,
                                         bg="medium purple",
                                         text="Score: " + self.board.score.get_score(),
                                         font=("courier", 20), anchor="s")
        self._score_displayer.grid(row=3, column=0, sticky="s", pady=40)

        self._seconds_left = INITIAL_SECS_LEFT
        self._timer = None
        self._play_again_button = None
        self.current_word = ""
        self.current_path = []
        self.buttons_that_are_clicked = []
        self.words_picked = []

    def check_word_func(self):
        """
        this function is called when the user clicks the button "check word".
        it uses the game's variables current path and current word and checks
         if the word is valid (using is_valid_path),
         if so it updates it.
         it also updates the score and enables the clicked buttons
        """
        for button in self.buttons_that_are_clicked:
            button["state"] = "active"
        if self.current_path:
            valid_word = helper.is_valid_path(self.board.board,
                                              self.current_path, WORDS_LIST)
            if valid_word and valid_word not in self.words_picked:
                if self.correct_words_displayer["text"]:
                    self.correct_words_displayer["text"] += "\n" + valid_word
                else:
                    self.correct_words_displayer["text"] += valid_word
                self.words_picked.append(valid_word)
                add_score = len(self.current_path) ** 2
                self.board.score.update_score(add_score)
                self._score_displayer[
                    "text"] = "Score: " + self.board.score.get_score()
        self.current_path = []
        self.current_word = ""
        self.buttons_that_are_clicked = []
        self.word_displayer["text"] = ""

    def timer_clicked(self):
        """
         is called when the user wants to begin a new round of the game,
        it destroys the "click here to start" button,
         creates the timer and changes the buttons to display the current board
        :return:
        """
        self._click_me.destroy()
        for i in range(BOARD_SIZE * BOARD_SIZE):
            button_clicked_arg = partial(self.button_clicked, i)
            self._buttons[i] = tk.Button(self.middle_frame_button_frame,
                                         text=self.board.board_dict[i],
                                         width=3, height=1,
                                         font=("Courier", 40), state="active",
                                         command=button_clicked_arg)
            self._buttons[i].grid(
                row=i // BOARD_SIZE,
                column=i % BOARD_SIZE, )
        timer_text = datetime.timedelta(minutes=3, seconds=0)
        self._timer = tk.Label(self._main_middle_frame, text=timer_text,
                               font=("courier", 30))
        self._timer.pack(side="top")
        self.update_time()

    def button_clicked(self, i):
        """
        when the user clicks the button,
        the location and letter are added to current path and current word
         and the button is disabled
        :param i: the index of the button in the board dictionary
        """
        path = (i // 4, i % 4)
        letter = self.board.board_dict[i]
        self.current_word += letter
        self.current_path.append(path)
        self._buttons[i]["state"] = "disable"
        self.buttons_that_are_clicked.append(self._buttons[i])
        self.word_displayer["text"] += letter

    def update_time(self):
        """
        this function is called repeatedly every second while the timer exists
        in order to update the time
        """
        mins, secs = divmod(self._seconds_left, 60)
        if 0 <= secs < 10:
            secs = "0" + str(secs)
        timer_text = str(0) + str(mins) + ":" + str(secs)
        self._timer["text"] = timer_text
        if self._seconds_left < 30:
            self._timer["bg"] = "red"
        if not self._seconds_left:
            self._timer["text"] = "GAME OVER!"
            self.end_game()
            return
        self._seconds_left -= 1
        self._timer.after(1000, self.update_time)

    def end_game(self):
        """
        when the timer is finished running,
        this function is called to ask the user whether they
         want to play again or end the game
        """
        for button in self._buttons:
            button.grid_forget()
        self._score_displayer[
            "text"] = "Score: " + self.board.score.get_score()
        self.word_displayer["activebackground"] = "RoyalBlue1"
        self.word_displayer["text"] = "Play Again"
        self.word_displayer["state"] = "active"
        self.word_displayer["command"] = self.play_again
        self._timer.destroy()
        self.check_word["text"] = "Click here to exit game"
        self.check_word["command"] = self.quit

    def play_again(self):
        """
        if the user chooses to play again this function creates a new round
        """
        self._click_me = tk.Button(self._main_middle_frame, width=20,
                                   height=3, text="Click here to begin!",
                                   font=("courier", 30),
                                   command=self.timer_clicked, bg="peach puff")
        self._click_me.pack(side="top")
        self._seconds_left = INITIAL_SECS_LEFT
        self.board = Board()
        self._score_displayer[
            "text"] = "Score: " + self.board.score.get_score()
        self.current_path = []
        self.current_word = ""
        self.words_picked = []
        self.correct_words_displayer["text"] = "Correct words: " + "\n"
        self.word_displayer["state"] = "disable"
        self.word_displayer["text"] = ""
        self.check_word.configure(command=self.check_word_func)
        self.check_word["text"] = "Check word"

    def quit(self):
        """
        if the user chooses to quit, this function destroys the game window
        """
        self.root.destroy()


def main():
    root = tk.Tk()
    root.geometry("1000x600")
    root.configure(bg="lemon chiffon")
    game_board = Board()
    MyGui(root, game_board)
    root.mainloop()


if __name__ == '__main__':
    main()
