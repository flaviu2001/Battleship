from save import Save
from domain import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font as tkfont
from ai import *
from game import Game
from settings import Settings


class Photo:
    def __init__(self, parent, path, relx, rely, relwidth, relheight, thing=tk.Label, antialias=False):
        self.thing = thing(parent)
        self.thing.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        self.thing.update()
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        if not antialias:
            image = Image.open(path)
        else:
            image = Image.open(path)
        image = image.resize((self.thing.winfo_width(), self.thing.winfo_height()), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.thing.configure(image=self.img)
        self.thing.image = self.img
        self.path = path

        def resize(event):
            new_image = Image.open(self.path)
            new_image = new_image.resize((event.width, event.height))
            self.img = ImageTk.PhotoImage(new_image)
            self.thing.configure(image=self.img)

        self.thing.bind("<Configure>", resize)

    def change(self, new_path):
        self.thing.update()
        self.path = new_path
        image = Image.open(self.path)
        image = image.resize((self.thing.winfo_width(), self.thing.winfo_height()))
        self.img = ImageTk.PhotoImage(image)
        self.thing.configure(image=self.img)

    def set_show(self):
        self.thing.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)

    def set_hidden(self):
        self.thing.place_forget()


class Tile:
    def __init__(self, parent, board, x, y, relx, rely, relheight, relwidth, thing, dictionary):
        self.x = x
        self.y = y
        self.parent = parent
        self.dictionary = dictionary
        self.board = board
        self.photo = Photo(parent,
                           self.dictionary[self.board[(self.x, self.y)]],
                           relx, rely, relheight, relwidth,
                           thing=thing)

    def update(self, dictionary=None):
        if dictionary is None:
            dictionary = self.dictionary
        if self.photo.path != dictionary[self.board[(self.x, self.y)]]:
            self.photo.change(dictionary[self.board[(self.x, self.y)]])


class TileAI(Tile):
    def __init__(self, parent, x, y, relx, rely, relheight, relwidth):
        Tile.__init__(self, parent, parent.gui.game.board_player,
                      x, y, relx, rely, relheight, relwidth, tk.Label, DICT_SPRITE)


class TilePlayer(Tile):
    def __init__(self, parent, x, y, relx, rely, relheight, relwidth):
        Tile.__init__(self, parent, parent.gui.game.board_ai,
                      x, y, relx, rely, relheight, relwidth, tk.Button, DICT_SPRITE_PLAYER)
        self.photo.thing.configure(command=self.shoot)
        if self.board[(x, y)] in (HIT, MISS, SUNK):
            self.photo.thing.configure(state="disabled")

    def shoot(self):
        self.parent.gui.game.player_move((self.x, self.y))
        matrix = self.parent.player
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j].update()
        self.photo.thing.configure(state="disabled")
        if self.parent.gui.game.board_ai.finished():
            self.parent.game_finished()
        elif self.parent.gui.game.turn == COMPUTER:
            self.parent.gui.game.ai_move()
            for i in range(len(self.parent.computer)):
                for j in range(len(self.parent.computer[i])):
                    self.parent.computer[i][j].update()
            if self.parent.gui.game.board_player.finished():
                self.parent.game_finished()


class PlayGame(tk.Frame):
    def __init__(self, parent, controller, gui):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.gui = gui
        color_bg = "#a2ddf5"
        color_active = "#7acef0"
        back_button = tk.Button(self, text="Back", font=40,
                                command=self.back_button,
                                bg=color_bg, activebackground=color_active)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        x_comp_begin = 0.1
        x_comp_end = 0.45
        y_comp_begin = 0.2
        y_comp_end = 0.9
        x_player_begin = 0.55
        x_player_end = 0.9
        y_player_begin = 0.2
        y_player_end = 0.9
        width = self.gui.game.board_player.width
        height = self.gui.game.board_player.height
        Photo(self, COMPUTER_SPRITE, 0.2, 0.12, 0.15, 0.055, antialias=True)
        Photo(self, PLAYER_SPRITE, 0.65, 0.12, 0.15, 0.055, antialias=True)
        self.win = Photo(self, WINNER_SPRITE, 0.3, 0.05, 0.35, 0.055, antialias=True)
        self.lose = Photo(self, LOSER_SPRITE, 0.3, 0.05, 0.35, 0.055, antialias=True)
        self.win.set_hidden()
        self.lose.set_hidden()
        self.computer = [[
            TileAI(self, i, j,
                   x_comp_begin + (x_comp_end - x_comp_begin) * (j / width),
                   y_comp_begin + (y_comp_end - y_comp_begin) * (i / height),
                   (x_comp_end - x_comp_begin) * (1 / width),
                   (y_comp_end - y_comp_begin) * (1 / height))
            for i in range(width)] for j in range(height)]
        if self.gui.game.turn == COMPUTER:
            self.gui.game.ai_move()
            for i in range(len(self.computer)):
                for j in range(len(self.computer[i])):
                    self.computer[i][j].update()
        self.player = [[
            TilePlayer(self, i, j,
                       x_player_begin + (x_player_end - x_player_begin) * (j / width),
                       y_player_begin + (y_player_end - y_player_begin) * (i / height),
                       (x_player_end - x_player_begin) * (1 / width),
                       (y_player_end - y_player_begin) * (1 / height))
            for i in range(width)] for j in range(height)]
        if self.gui.game.board_player.finished():
            self.game_finished()

    def game_finished(self):
        if self.gui.game.board_player.finished():
            self.lose.set_show()
        else:
            self.win.set_show()
        for i in range(len(self.player)):
            for j in range(len(self.player[i])):
                self.player[i][j].photo.thing.configure(state="disabled")
                self.player[i][j].update(DICT_SPRITE)

    def back_button(self):
        game = Save(game=self.gui.game).load()
        if not game:
            self.controller.frames["MainMenu"].button2.configure(state="disabled")
        else:
            self.controller.frames["MainMenu"].button2.configure(state="normal",
                                                                 command=lambda: self.controller.frames["MainMenu"].
                                                                 continue_game(game))
        self.controller.show_frame("MainMenu")


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        color_bg = "#a2ddf5"
        color_active = "#7acef0"
        back_button = tk.Button(self, text="Back", font=40,
                                command=self._back_button,
                                bg=color_bg, activebackground=color_active)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)

        choices_size = ["Board size: Default", "Board size: Small", "Board size: Normal"]
        self.variable_size = tk.StringVar(self)
        self.variable_size.set(choices_size[0])
        option_size = tk.OptionMenu(self, self.variable_size, *choices_size)
        option_size.configure(font=40, bg=color_bg, activebackground=color_active)
        option_size.place(relx=0.2, rely=0.2, relheight=0.07, relwidth=0.3)
        option_size["menu"].configure(bg=color_bg, activebackground=color_active, font=40)

        choices_difficulty = ["Difficulty: Easy", "Difficulty: Normal", "Difficulty: Advanced"]
        self.variable_difficulty = tk.StringVar(self)
        ai_string = Settings().ai()
        if ai_string == "easy":
            self.variable_difficulty.set(choices_difficulty[0])
        elif ai_string == "normal":
            self.variable_difficulty.set(choices_difficulty[1])
        else:
            self.variable_difficulty.set(choices_difficulty[2])
        option_difficulty = tk.OptionMenu(self, self.variable_difficulty, *choices_difficulty)
        option_difficulty.configure(font=40, bg=color_bg, activebackground=color_active)
        option_difficulty.place(relx=0.2, rely=0.35, relheight=0.07, relwidth=0.3)
        option_difficulty["menu"].configure(bg=color_bg, activebackground=color_active, font=40)

        choices_first = ["First to move: Player", "First to move: Computer", "First to move: Random"]
        self.variable_first = tk.StringVar(self)
        first = Settings().first()
        if first == "player":
            self.variable_first.set(choices_first[0])
        elif first == "computer":
            self.variable_first.set(choices_first[1])
        else:
            self.variable_first.set(choices_first[2])
        option_first = tk.OptionMenu(self, self.variable_first, *choices_first)
        option_first.configure(font=40, bg=color_bg, activebackground=color_active)
        option_first.place(relx=0.2, rely=0.5, relheight=0.07, relwidth=0.3)
        option_first["menu"].configure(bg=color_bg, activebackground=color_active, font=40)

    def _back_button(self):
        size = self.variable_size.get()
        if size == "Board size: Small":
            Settings().set_height(8)
            Settings().set_width(8)
            Settings().set_ships({CARRIER: 0, BATTLESHIP: 1, CRUISER: 1, DESTROYER: 1})
        elif size == "Board size: Normal":
            Settings().set_height(10)
            Settings().set_width(10)
            Settings().set_ships({CARRIER: 1, BATTLESHIP: 1, CRUISER: 2, DESTROYER: 1})
        difficulty = self.variable_difficulty.get()
        if difficulty == "Difficulty: Easy":
            Settings().set_ai("easy")
        elif difficulty == "Difficulty: Normal":
            Settings().set_ai("normal")
        else:
            Settings().set_ai("advanced")
        first = self.variable_first.get()
        if first == "First to move: Player":
            Settings().set_first("player")
        elif first == "First to move: Computer":
            Settings().set_first("computer")
        else:
            Settings().set_first("random")
        self.controller.show_frame("MainMenu")


class MainMenu(tk.Frame):
    def __init__(self, parent, controller, gui):
        tk.Frame.__init__(self, parent)
        color_bg = "#a2ddf5"
        color_active = "#7acef0"
        self.parent = parent
        self.controller = controller
        self.gui = gui
        Photo(self, "sprites/battleship_logo.png", 0.3, 0.07, 0.4, 0.2)
        button1 = tk.Button(self, text="New Game", font=40,
                            command=self.new_game,
                            bg=color_bg, activebackground=color_active)
        button1.place(relx=0.4, rely=0.33, relheight=0.15, relwidth=0.2)
        game = Save(game=self.gui.game).load()
        self.button2 = tk.Button(self, text="Continue Game", font=40,
                                 command=lambda: self.continue_game(game),
                                 bg=color_bg, activebackground=color_active)
        self.button2.place(relx=0.4, rely=0.53, relheight=0.15, relwidth=0.2)
        if not game:
            self.button2.configure(state="disabled")
        button3 = tk.Button(self, text="Settings", font=40,
                            command=lambda: controller.show_frame("SettingsPage"),
                            bg=color_bg, activebackground=color_active)
        button3.place(relx=0.4, rely=0.73, relheight=0.15, relwidth=0.2)

    def continue_game(self, game):
        self.gui.game = game
        frame = PlayGame(parent=self.parent, controller=self.controller, gui=self.gui)
        self.controller.frames["PlayGame"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame("PlayGame")

    def new_game(self):
        ai_string = Settings().ai()
        if ai_string == "easy":
            ai = EasyAI
        elif ai_string == "normal":
            ai = NormalAI
        else:
            ai = AdvancedAI
        board_ai = Board()
        board_player = Board(owner=PLAYER)
        first_string = Settings().first()
        if first_string == "player":
            first = PLAYER
        elif first_string == "computer":
            first = COMPUTER
        else:
            first = random.choice((PLAYER, COMPUTER))
        self.gui.game = Game(ai, board_player, board_ai, first)
        frame = PlayGame(parent=self.parent, controller=self.controller, gui=self.gui)
        self.controller.frames["PlayGame"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame("PlayGame")


class WindowMaster(tk.Tk):
    def __init__(self, gui):
        tk.Tk.__init__(self)
        self.gui = gui
        self.geometry("900x600")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Battleship")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (MainMenu, SettingsPage):
            page_name = F.__name__
            if F in (MainMenu,):
                frame = F(parent=container, controller=self, gui=gui)
            else:
                frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class GUI:
    def __init__(self):
        self._game = None

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, new_game):
        self._game = new_game

    def start(self):
        WindowMaster(self).mainloop()