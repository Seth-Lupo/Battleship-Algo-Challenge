from doctest import Example
from players import *
from game import *
from gui import *
from test import *

class TemplatePlayer(Player):

    def __init__(self):
        super().__init__()

    def setup(self):

        self.current_game.place_ship(self, Ship((0,1), 4, COLUMNWISE))
    
        self.current_game.view_own_ships(self)
        
        self.current_game.view_own_private_board(self) 
        EMPTY
        SHIP
        
        self.current_game.view_own_public_board(self)
        self.current_game.view_enemy_board(self)
        EMPTY
        HIT
        MISS
        SUNKEN
        
    def play(self):
        pass
  
    def review(self):
        pass

if __name__ == "__main__":
    p1 = TemplatePlayer()
    p2 = Player()
    g = VisibleGame(p1, p2, 200)
    print(type(g.play()).__name__)