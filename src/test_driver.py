import sys

from models import *
from loguru import logger

# tiles = TilesGenerator().generate()
# bag = Bag(tiles, initial_shuffle=False)
#
# bag._print()
# bag.shuffle()
# bag._print()
#

logger.remove()
# logger.add(sys.stderr, level="INFO")
logger.add(sys.stderr, level="DEBUG")

game = Game()
game.print_board()
game.print_scoreboard()
game.play()
