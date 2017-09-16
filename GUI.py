from tkinter import *
import gameLogic
import checkersException
from functools import partial
from tkinter import messagebox
import bot


class Advanced_Button(Button):

    def __init__(self, pos_x, pos_y, master = None):
        Button.__init__(self, master)
        self.pos_x = pos_x
        self.pos_y = pos_y


class Basic_Users_interface():

    def check_winner(self):
        res = self.game.initialize_win()
        if res != None:
            self.bot.bod_mode = False;
            if res == 'first':
                messagebox.showinfo('Message', 'Rad win')
            else:
                messagebox.showinfo('Message', 'Blue win')
            self.root.quit()

    def take_chip(self, x, y):
        try:
            if self.progress % 2 == 1:
                self.game.first_player.take_chip(x, y)
            else:
                self.game.second_player.take_chip(x, y)
        except checkersException.InvalidTakeChipsException:
            messagebox.showinfo('Error', 'The wrong chip is taken')
            return
        except checkersException.InvalidEndJump:
            messagebox.showinfo('Error', 'Your move is not completed ')
            return

    def make_jump(self, x, y):
        try:
            if self.progress % 2 == 1:
                result_jump = self.game.first_player.make_jump(x, y)
                self.progress += result_jump
            else:
                result_jump = self.game.second_player.make_jump(x, y)
                print(result_jump)
                self.progress += result_jump
            self.check_winner()
        except checkersException.InvalidJump:
            messagebox.showinfo('Error', 'Wrong move')
            return
        except checkersException.InvalidJumpAttack:
            messagebox.showinfo('Error', 'You need attack enemy')
            return
        if result_jump != 0 and self.human != None and self.bot.bot_mode == True:
            try:
                self.progress += self.bot.bot_do()
            except ValueError:
                self.check_winner()
        self.draw()

    def draw(self):
        for x in range(0, 10):
            start_step = 1
            if x % 2 == 1:
                start_step = 0
            for y in range(start_step, 10, 2):
                pos_x = x
                pos_y = y
                if type(self.game.field[x][y]) == gameLogic.Chip:
                    self.list_button[x][y]['command'] = partial(self.take_chip, pos_x, pos_y)
                    if self.game.field[x][y].party == 'white':
                        if self.game.field[x][y].is_king:
                            img = PhotoImage(file='image/firstK.gif')
                        else:
                            img = PhotoImage(file='image/first.gif')
                    else:
                        if self.game.field[x][y]. is_king:
                            img = PhotoImage(file='image/secondK.gif')
                        else:
                            img = PhotoImage(file='image/second.gif')
                else:
                    self.list_button[x][y]['command'] = partial(self.make_jump, pos_x, pos_y)
                    img = PhotoImage(file='image/black.gif')
                self.list_save_image.append(img)
                self.list_button[x][y]['image'] = img

    def __init__(self, root, party=None):
        self.game = gameLogic.PlayingField()
        self.first_player = self.game.first_player
        self.second_player = self.game.second_player
        self.human = party
        self.root = root
        self.list_button = []
        self.list_save_image = []
        self.progress = 1
        for x in range(0, 10):
            new_line = []
            for y in range(0, 10):
                new_line.append(Advanced_Button(x, y, self.root))
                img = PhotoImage(file='image/white.gif')
                self.list_save_image.append(img)
                new_line[y]['image'] = img
            self.list_button.append(new_line)
        if (party != None):
            if party == 'first':
                self.bot = bot.Bot(self.second_player)
            else:
                self.bot = bot.Bot(self.first_player)
                print('before', self.progress)
                self.progress += self.bot.bot_do()
                print('after', self.progress)
        self.draw()

        for x in range(0, 10):
            for y in range(0, 10):
                self.list_button[x][y].grid(row=x, column=y)
        self.root.mainloop()


class GameMenu():

    def __init__(self, root):
        self.list_image = []
        self.root = root
        self.draw_menu(self.root)

    def start_game(self, party, root):
        self.clear_form(root)
        basic_game = Basic_Users_interface(root, party)

    def clear_form(self, root):
        widget_list = root.grid_slaves()
        for widget in widget_list:
            widget.destroy()

    def take_party(self, root):
        self.clear_form(root)
        img_first = PhotoImage(file='image/first.gif')
        self.list_image.append(img_first)
        img_second = PhotoImage(file='image/second.gif')
        self.list_image.append(img_second)
        first_player = Button(root, text='Red', image=img_first, command=partial(self.start_game, 'first', root))
        second_player = Button(root, text='Blue', image=img_second, command=partial(self.start_game, 'second', root))
        back = Button(root, text='Back', width=5, command=partial(self.draw_menu, root))
        Label(text='Change party').grid(row=0, column=1, padx=8, pady=20)
        first_player.grid(row=1, column=0, pady=20, padx=8)
        second_player.grid(row=1, column=2, pady=20, padx=8)
        back.grid(row=2, column=1, pady=10, padx=8)

    def draw_menu(self, root):
        self.clear_form(root)
        take_mode_single = Button(root, text='Single mode', width=10, height=3, command=partial(self.take_party, root))
        take_mode_coop = Button(root, text='Coop mode', width=10, height=3, command=partial(self.start_game, None, root))
        quit = Button(root, text='Quit', width=10, height=3, command=lambda: self.root.quit())
        canvas = Canvas(height=200, width=300)
        img = PhotoImage(file='image/main.gif')
        self.list_image.append(img)
        canvas.create_image(169, 100, image=img)
        take_mode_single.grid(row=0, pady=10, padx=8)
        take_mode_coop.grid(row=1, pady=10, padx=8)
        quit.grid(row=2, pady=10, padx=8)
        canvas.grid(row=0, rowspan=3, column=1, padx=8)

if __name__=="__main__":
    mode = ''
    root = Tk()
    menu = GameMenu(root)
    root.mainloop()

