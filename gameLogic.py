import checkersException as exc


class Chip:

    def __init__(self, pos_x, pos_y, enemy_party, player):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.party = player.party
        self.enemy_party = enemy_party
        self.chips_for_fight = {}
        self.my_lord = player
        self.is_king = False


class Player():

    def __init__(self, party, field):
        self.party = party
        self.field = field
        self.chips_for_fight = []
        self.active_chip = None
        self.player_chips = []
        self.is_block = False
        self.big_list_step = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def add_chip(self, chip):
        self.player_chips.append(chip)

    def remove_chip(self, chip):
         self.player_chips.remove(chip)

    def get_step_list(self, chip):
        if chip.is_king:
            return self.big_list_step
        return [1]

    def take_chip(self, pos_x, pos_y):
        if self.is_block:
            raise exc.InvalidEndJump
        chip = self.field[pos_x][pos_y]
        self.chips_for_fight.clear()
        if chip in self.player_chips:
            self.active_chip = chip
            list_for_step = self.get_step_list(self.active_chip)
            self.check_chips_for_fight(self.active_chip, list_for_step)
            self.analyze_game()
        else:
            raise exc.InvalidTakeChipsException

    def analyze_game(self):
        for x in range(0, 10):
            start_step = 1
            if x % 2 == 1:
                start_step = 0
            for y in range(start_step, 10, 2):
                if type(self.field[x][y]) == Chip:
                    self.field[x][y].chips_for_fight.clear()
                    list_for_step = self.get_step_list(self.field[x][y])
                    self.check_chips_for_fight(self.field[x][y], list_for_step)
                    if len(self.field[x][y].chips_for_fight) != 0 and self.party == self.field[x][y].party:
                        self.chips_for_fight.append(self.field[x][y])

    def is_correctness_coord(self, x, y):
        if (y >= len(self.field)) or (y < 0):
            return False
        if (x >= len(self.field)) or (x < 0):
            return False
        return True


    def check_path(self, chip, x, y):
        step_x = (x - chip.pos_x)// abs(x - chip.pos_x)
        step_y = (y - chip.pos_y)// abs(y - chip.pos_y)
        start_pos_x = chip.pos_x + step_x
        start_pos_y = chip.pos_y + step_y
        while start_pos_x != x and start_pos_y != y:
            if type(self.field[start_pos_x][start_pos_y]) == Chip:
                return False
            start_pos_x = start_pos_x + step_x
            start_pos_y = start_pos_y + step_y
        return True

    def check_conditions(self, chip, x, y):
        if (abs(x) == abs(y)) and self.is_correctness_coord(chip.pos_x + x, chip.pos_y + y):
            if type(self.field[chip.pos_x + x][chip.pos_y + y]) == Chip and self.is_correctness_coord(
                                    chip.pos_x + x + (x // abs(x)), chip.pos_y + y + y // abs(y)):
                if self.field[chip.pos_x + x][chip.pos_y + y].party == chip.enemy_party:
                    enemy = self.field[chip.pos_x + x][chip.pos_y + y]
                    enemy_neighborhood = self.field[chip.pos_x + x + x // abs(x)][chip.pos_y + y + y // abs(y)]
                    if enemy_neighborhood == 0:
                        if self.check_path(chip, chip.pos_x + x, chip.pos_y + y):
                            chip.chips_for_fight[(chip.pos_x + x + x // abs(x), chip.pos_y + y + y // abs(y))] = enemy

    def check_chips_for_fight(self, chip, list_step):
        for step in list_step:
            for x in range(-1 * step,  step + 1):
                for y in range(-1 * step,  step + 1):
                    if (x == 0) or (y == 0):
                        continue
                    self.check_conditions(chip, x, y)


    def delete_enemy(self, enemy):
        enemy.my_lord.player_chips.remove(enemy)
        self.field[enemy.pos_x][enemy.pos_y] = 0

    def do_jump(self, pos_x, pos_y, operation):
        self.field[pos_x][pos_y] = self.active_chip
        self.field[self.active_chip.pos_x][self.active_chip.pos_y] = 0
        self.active_chip.pos_x = pos_x
        self.active_chip.pos_y = pos_y
        if self.active_chip.is_king:
            list_for_step = self.big_list_step
        else:
            list_for_step = [1]
        self.check_chips_for_fight(self.active_chip, list_for_step)
        if len(self.active_chip.chips_for_fight) and operation == 'attack':
            self.is_block = True
            return 0
        self.it_chip_is_king(self.active_chip)
        self.is_block = False
        return 1

    def it_chip_is_king(self, chip):
         if chip.party == 'white' and chip.pos_x == 9:
             chip.is_king = True
         if chip.party == 'black' and chip.pos_x == 0:
             chip.is_king = True

    def make_jump(self, pos_x, pos_y):
        if len(self.chips_for_fight) > 0:
            if len(self.active_chip.chips_for_fight) != 0 and self.active_chip in self.chips_for_fight:
                if ((pos_x, pos_y) in self.active_chip.chips_for_fight.keys()):
                    self.delete_enemy(self.active_chip.chips_for_fight[(pos_x, pos_y)])
                    self.active_chip.chips_for_fight.clear()
                    return self.do_jump(pos_x, pos_y, 'attack')
                else:
                    raise exc.InvalidJumpAttack
            else:
                raise exc.InvalidJumpAttack
        is_correct_jump = self.is_correctness_coord(pos_x,  pos_y)
        if (abs(self.active_chip.pos_x - pos_x) + abs(self.active_chip.pos_y - pos_y)) == 2 and is_correct_jump:
            return self.do_jump(pos_x, pos_y, 'run')
        if (abs(self.active_chip.pos_x - pos_x) + abs(self.active_chip.pos_y - pos_y)) % 2 == 0 and is_correct_jump and self.field[self.active_chip.pos_x][self.active_chip.pos_y].is_king:
            return self.do_jump(pos_x, pos_y, 'run')
        else:
            raise exc.InvalidJump


class PlayingField():

    def __init__(self):
        self.init_field()
        self.init_white()
        self.init_black()

    def init_field(self):
        self.field = []
        self.height = 10
        self.width = 10
        for x in range(0, self.height):
            new_line = []
            self.field.append(new_line)
            for y in range(0, self.width):
                new_line.append(0)

    def init_white(self):
        self.first_player = Player('white', self.field)
        self.put_chips(0, 4, 1, 10, 'black', self.first_player)
        self.put_chips(1, 4, 0, 10, 'black', self.first_player)

    def init_black(self):
        self.second_player = Player('black', self.field)
        self.put_chips(6, 10, 1, 10, 'white', self.second_player)
        self.put_chips(7, 10, 0, 10, 'white', self.second_player)

    def put_chips(self, start_x, finish_x, start_y, finish_y, enemy_party, player):
        for x in range(start_x, finish_x, 2):
            for y in range(start_y, finish_y, 2):
                new_chip = Chip(x, y, enemy_party, player)
                self.field[x][y] = new_chip
                player.player_chips.append(new_chip)

    def initialize_win(self):
        if len(self.first_player.player_chips) == 0:
            return 'second'
        if len(self.second_player.player_chips) == 0:
            return 'first'


def main():
    board = PlayingField()
    for x in range(0, 10):
        my_list = []
        for y in range(0, 10):
            my_list.append(board.field[x][y])

if __name__=="__main__":
    main()

