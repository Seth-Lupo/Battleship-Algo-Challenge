from math import floor
from random import randrange
from numpy import place
from game import *

class Player:
    
    def __init__(self):
        self.current_game = None

    def set_game(self, game):
        self.current_game = game

    def setup(self):
        
        remaining_ships = list(FLEET_TEMPLATE)
        while remaining_ships:
            
            length = remaining_ships[-1]
            dir = randrange(2)
            row = randrange(10)
            col = randrange(10)
            ship = Ship((row, col), length, dir)

            success = self.current_game.place_ship(self, ship)
            if success:
                remaining_ships.pop()


    def play(self):

        coordinate = None
        while True:
            board = self.current_game.view_enemy_board(self)
            row = randrange(10)
            col = randrange(10)
            if board[row][col] == EMPTY:
                coordinate = (row, col)
                break

        self.current_game.shoot_enemy(self, coordinate)

  



       
        

       
        
        
        
