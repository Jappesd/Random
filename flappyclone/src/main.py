from game import Game
import os
import sys
from utils import resource_path

print("FILE:", __file__)
print("DIR :", os.path.dirname(__file__))
print("ROOT:", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print("ASSET:", resource_path("assets/pipecap.png"))

if __name__ == "__main__":
    game = Game()
    game.run()
