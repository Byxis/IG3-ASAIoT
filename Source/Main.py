from Class.Game import Game
from Utils.API_Raspberry import *
from time import sleep

def main():
    game = Game(input("Enter your name: "))
    game.play()

if __name__ == "__main__":
    main()
