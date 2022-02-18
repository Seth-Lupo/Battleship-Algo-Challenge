from xmlrpc.client import boolean
import numpy as np
from itertools import *
from copy import *

EMPTY = 0
SHIP = 1
MISS = 2
HIT = 3
SUNKEN = 4

ROWWISE = 1
COLUMNWISE = 0

BOARD_SHAPE = (10, 10)



FLEET_TEMPLATE = (5,4,3,3,2)

def tuple_in_bounds(T, t):
    return  t[0] >= 0 and t[1] >= 0 and t[0] < T[0] and t[1] < T[1]

class Ship:
    
    def __init__(self, position, length, direction):
        
        self.position = position
        self.length = length
        self.direction = direction

        self.coordinates = []
        for i in range(0, length):
            self.coordinates += [ (position[0] + (1-direction)*i, position[1] + direction*i) ]

        self.original_coordinates = self.coordinates.copy()

        self.sunken = False
        self.legal = tuple_in_bounds(BOARD_SHAPE, self.coordinates[0]) and tuple_in_bounds(BOARD_SHAPE, self.coordinates[-1])
        

    def hit(self, coordinate):
        
        self.coordinates.remove(coordinate)
        
        if not self.coordinates:
            self.sunken = True


class Board:

    def __init__(self, owner):
        
        self.owner = owner
        self.legal = False
        
        self.hidden_arr = np.zeros(shape=BOARD_SHAPE)
        self.visible_arr = np.zeros(shape=BOARD_SHAPE)

        self.fleet = []
        self.remaining_ships = list(FLEET_TEMPLATE)

    def place_ship(self, ship):
        
        if not ship.legal:
            return False

        if not ship.length in self.remaining_ships:
            return False
            
        for other_ship in self.fleet:
            if set(ship.coordinates) & set(other_ship.coordinates):
                return False
        
        self.remaining_ships.remove(ship.length)
        self.fleet += [ship]

        for coordinate in ship.coordinates:
            row, col = coordinate
            self.hidden_arr[row][col] = SHIP

        return True

        
    def confirm(self):
        if len(self.remaining_ships) == 0:
            self.legal = True


    def shoot(self, coordinate):
        
        row, col = coordinate
        if self.hidden_arr[row][col] == SHIP:
            
            self.visible_arr[row][col] = HIT

            ship = self.ship_by_coordinate((coordinate))
            ship.coordinates.remove(coordinate)
            if not ship.coordinates:
                self.sink_ship(ship)

        else:
            self.visible_arr[row][col] = MISS


    def fleet_alive(self):
        for ship in self.fleet:
            if not ship.sunken:
                return True
        return False
        

    def sink_ship(self, ship):
        for coordinate in ship.original_coordinates:
            row, col = coordinate
            self.visible_arr[row][col] = SUNKEN
        ship.sunken = True

    def ship_by_coordinate(self, coordinate):
        for ship in self.fleet:
            if coordinate in ship.coordinates:
                return ship
        
class Game:

    def __init__(self, player1, player2):
        
        self._player1 = player1
        self._player2 = player2

        self._player1.current_game = self
        self._player2.current_game = self

        self._winner = None

        self._turns = 0
        
        self._own_board = {
            player1 : Board(player1),
            player2 : Board(player2),
        }

        self._enemy_board = {
            self._player1 : self._own_board[self._player2],
            self._player2 : self._own_board[self._player1],
        }

        self._other_player = {
            self._player1 : self._player2,
            self._player2 : self._player1
        } 

    def setup(self):
        self._player1.set_game(self)
        self._player2.set_game(self)
        self._player1.setup()
        self._player2.setup()
        self._own_board[self._player1].confirm()
        self._own_board[self._player2].confirm()

    def play(self):
        for i in range(0, 2*BOARD_SHAPE[0]*BOARD_SHAPE[1]):
            self._player1.play()
            if self._winner:
                return self._player1
            self._player2.play()
            if self._winner:
                return self._player2

    def view_own_board(self, player):
        return self._own_board[player].hidden_arr.copy()

    def view_enemy_board(self, player):
        return self._enemy_board[player].visible_arr.copy()

    def view_ships(self, player):
        return deepcopy(self._own_board[player].fleet)

    def place_ship(self, player, ship):
        return self._own_board[player].place_ship(ship)

    def shoot_enemy(self, player, coordinate):
        
        row, col = coordinate
        board = self._enemy_board[player]
        
        if not board.legal:
            self._winner = player
            return False

        if not tuple_in_bounds(BOARD_SHAPE, coordinate):
            self._winner = self._other_player[player]
            return False
        
        if not board.visible_arr[row][col] == EMPTY:
            self._winner = self._other_player[player]
            return False

        board.shoot(coordinate)

        if not board.fleet_alive():
            self._winner = player
        
        return True


