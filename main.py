from display import Display
from game import Game

if __name__ == "__main__":
    display = Display()
    game = Game(display)
    game.run()
