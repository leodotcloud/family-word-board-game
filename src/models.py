import random
from loguru import logger

from defaults import *
from characters import *


class Tile:
    def __init__(self, value, score, blank_value=DEFAULT_BLANK_VALUE):
        self.value = value
        self.score = score
        self.blank_value = blank_value

    def print(self):
        print(self.value, end="")

    def is_blank(self):
        return self.value == self.blank_value

    def __str__(self):
        return self.value


class TilesGenerator:
    def __init__(self, distribution=DEFAULT_LETTER_DISTRIBUTION):
        logger.debug('TilesGenerator: created')
        self.distribution = distribution

    def generate(self):
        logger.debug('TilesGenerator: generating')
        tiles = []
        for letter in self.distribution:
            for i in range(0, letter[1]):
                tiles.append(Tile(letter[0], letter[2]))

        return tiles


class Cell:
    def __init__(self, cell_multiplier=None, word_multiplier=None):
        self.cell_multiplier = cell_multiplier
        self.word_multiplier = word_multiplier
        self.tile = None

    def place_tile(self, tile):
        self.tile = tile

    def __str__(self):
        if self.tile:
            return self.tile
        else:
            if not self.cell_multiplier and not self.word_multiplier:
                return FW_SPACE

            if self.cell_multiplier == 2:
                return FW_PARENTHESIZED_TWO
            elif self.cell_multiplier == 3:
                return FW_PARENTHESIZED_THREE
            elif self.word_multiplier == 2:
                return FW_CIRCLED_TWO
            elif self.word_multiplier == 3:
                return FW_CIRCLED_THREE


class GridGenerator:
    def __init__(self, n_rows, n_cols, multipliers):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.multipliers = multipliers

    def generate(self):
        grid = []
        for r in range(self.n_rows):
            row = []
            for c in range(self.n_cols):
                cell_multiplier = None
                word_multiplier = None

                if "DL" == self.multipliers[r][c]:
                    cell_multiplier = 2
                elif "TL" == self.multipliers[r][c]:
                    cell_multiplier = 3
                elif "DW" == self.multipliers[r][c]:
                    word_multiplier = 2
                elif "TW" == self.multipliers[r][c]:
                    word_multiplier = 3

                cell = Cell(cell_multiplier, word_multiplier)
                row.append(cell)
            grid.append(row)
        return grid


class Board:
    def __init__(self, n_rows=DEFAULT_BOARD_ROW_SIZE, n_cols=DEFAULT_BOARD_COL_SIZE):
        self.n_rows = n_rows
        self.n_cols = n_cols
        # self.grid = [[Cell() for col in range(self.n_cols)] for row in range(self.n_rows)]
        self.grid = GridGenerator(n_rows, n_cols, DEFAULT_BOARD_MULTIPLIERS).generate()
        logger.debug(self.grid)

    def print(self):
        for i, row in enumerate(self.grid):
            # Print the top border
            if i == 0:
                print(BOX_CHAR_TOP_LEFT + (BOX_CHAR_HORIZONTAL_LINE + FW_HORIZONTAL_LINE + BOX_CHAR_HORIZONTAL_LINE + BOX_CHAR_TOP_MIDDLE) * (len(row) - 1) + (
                            BOX_CHAR_HORIZONTAL_LINE + FW_HORIZONTAL_LINE + BOX_CHAR_HORIZONTAL_LINE) + BOX_CHAR_TOP_RIGHT)
            # Print each row
            print(BOX_CHAR_VERTICAL_LINE + " " + (" " + BOX_CHAR_VERTICAL_LINE + " ").join(str(cell) for cell in row) + " " + BOX_CHAR_VERTICAL_LINE)
            # Print the bottom border
            if i == len(self.grid) - 1:
                print(BOX_CHAR_BOTTOM_LEFT + (BOX_CHAR_HORIZONTAL_LINE + FW_HORIZONTAL_LINE + BOX_CHAR_HORIZONTAL_LINE + BOX_CHAR_BOTTOM_MIDDLE) * (len(row) - 1) + (
                            BOX_CHAR_HORIZONTAL_LINE + FW_HORIZONTAL_LINE + BOX_CHAR_HORIZONTAL_LINE) + BOX_CHAR_BOTTOM_RIGHT)
            else:
                print(
                    BOX_CHAR_LEFT_MIDDLE + (BOX_CHAR_HORIZONTAL_LINE + FW_HORIZONTAL_LINE + BOX_CHAR_HORIZONTAL_LINE + BOX_CHAR_MIDDLE_CROSS) * (len(row) - 1) + (BOX_CHAR_HORIZONTAL_LINE + FW_HORIZONTAL_LINE + BOX_CHAR_HORIZONTAL_LINE) + BOX_CHAR_RIGHT_MIDDLE)


class Rack:
    def __init__(self, max_size=DEFAULT_RACK_MAX_SIZE):
        self.max_size = max_size
        self.tiles = []

    def print(self):
        print("Rack: ", end="")
        print(' '.join(str(t) for t in self.tiles))

    def _shuffle_algo_1_simple(self):
        tmp = []
        while self.tiles:
            i = random.randint(0, len(self.tiles) - 1)
            tmp.append(self.tiles.pop(i))

        self.tiles = tmp

    def shuffle(self):
        return self._shuffle_algo_1_simple()

    def add_tiles(self, tiles):
        logger.debug("adding tiles: {}", str(tiles))
        self.tiles.extend(tiles)

    def replenish_count(self):
        return self.max_size - len(self.tiles)

    def empty_all(self):
        logger.debug("emptying tiles: {}", self.tiles)
        tmp = self.tiles
        self.tiles = []
        return tmp

    def get_toss_tile(self):
        if len(self.tiles) > 0:
            return self.tiles[0]
        else:
            return []


class Bag:
    def __init__(self, tiles=None,
                 initial_shuffle=True,
                 shuffle_after_draw=True,
                 shuffle_after_put_back=True,
                 ):
        if tiles is None:
            tiles = TilesGenerator().generate()
        self.tiles = tiles
        self.shuffle_after_draw = shuffle_after_draw
        self.shuffle_after_put_back = shuffle_after_put_back

        if initial_shuffle:
            self.shuffle()

    def _shuffle_algo_1_simple(self):
        tmp = []
        while self.tiles:
            i = random.randint(0, len(self.tiles) - 1)
            tmp.append(self.tiles.pop(i))

        self.tiles = tmp

    def shuffle(self):
        self._shuffle_algo_1_simple()

    def _print(self):
        count = 0
        print(f'Bag: (Total: {len(self.tiles)})')
        for tile in self.tiles:
            tile.print()
            count += 1
            if count > 9:
                print("")
                count = 0

    def _draw_algo_1_simple(self, count):
        tiles = []
        while count > 0 and len(self.tiles) > 0:
            logger.debug("number_of_tiles: {}", len(self.tiles))
            i = random.randint(0, len(self.tiles) - 1)
            logger.debug("popping i={}", i)
            tiles.append(self.tiles.pop(i))
            count -= 1
        return tiles

    # Ensures no blank is drawn
    def draw_toss(self):
        blanks = []
        while len(self.tiles) > 0:
            tiles = self.draw()
            if tiles[0].is_blank():
                blanks.extend(tiles)
            else:
                return tiles

        if blanks:
            self.tiles.extend(blanks)
        return []

    def draw(self, count):
        tiles = self._draw_algo_1_simple(count)
        if self.shuffle_after_draw:
            self.shuffle()
        return tiles

    def put_back(self, tiles):
        self.tiles.extend(tiles)
        if self.shuffle_after_put_back:
            self.shuffle()


class Player:
    def __init__(self, name, bag):
        self.name = name
        self.rack = Rack()
        self.bag = bag
        self.score = 0

    def draw_toss(self):
        self.rack.add_tiles(self.bag.draw(1))

    def empty_rack(self):
        print(f"Player: {self.name} emptying rack")
        return self.rack.empty_all()

    def draw(self):
        count = self.rack.replenish_count()
        print(f"Player: {self.name} drawing {count} tiles")
        self.rack.add_tiles(self.bag.draw(count))

    def get_score(self):
        return self.score

    def add_to_score(self, score):
        self.score += score

    def print_rack(self):
        print(f"Player: {self.name}")
        self.rack.print()

    def shuffle_rack(self):
        self.rack.shuffle()

class Game:
    def __init__(self, num_players=DEFAULT_NUM_PLAYERS):
        self.num_players = num_players
        self.bag = Bag()
        self.board = Board()
        self.players = [Player(DEFAULT_PLAYER_NAMES[i], self.bag) for i in range(0, num_players)]
        self.current_player_index = None

    def do_toss(self):
        print("Time for a toss")
        for p in self.players:
            p.draw_toss()

        self._pick_toss_winner()

        for p in self.players:
            p.empty_rack()

        self.current_player_index = 0
    #
    # Picked by alphabetical order of value.
    # If there is a tie, pick based on alphabetical order of name.
    #
    def _toss_picking_algo_1_simple(self):
        self.players = sorted(self.players, key=lambda x: (x.rack.get_toss_tile().value, x.name))

    def _pick_toss_winner(self):
        for p in self.players:
            print(f"{p.name} picked: {p.rack.get_toss_tile().value}")

        self._toss_picking_algo_1_simple()

        print("Toss winner: ", self.players[0].name)

        print("Play order: ")
        for p in self.players:
            print(f"{p.name}  ")

    def print_board(self):
        self.board.print()

    def get_scoreboard(self):
        return [(p.name, p.score) for p in self.players]

    def print_scoreboard(self):
        sb = self.get_scoreboard()

        print("Scoreboard: ")
        print("===================================")
        print("Player Name                   Score")
        print("-----------------------------------")
        for entry in sb:
            print("{:26}   {:4d}".format(entry[0], entry[1]))
        print("===================================")

    def do_first_draws(self):
        print("First draw of tiles")
        for p in self.players:
            p.draw()
        print("")

    def play_first_word(self):
        self.players[self.current_player_index].print_rack()

    def play(self):
        self.do_toss()
        self.do_first_draws()

        self.play_first_word()
