from players import *
from game import *
from gui import *
from test import *

class TemplatePlayer(Player):

    # What is run when your bot is initialized. 
    # It will be initialized each match. However, it will retain its memory from previous game.
    # It might be helpful to have a memory of your opponents strategy....


    def __init__(self):
        super().__init__()

        # setup() will be called every game. It is where you will place all of your ships.
        # By default, it will scatter the ships randomly.
        # If you fail to place all of your ships you will lose.

        
        

    def setup(self):
        
        # You'll have two boards which you can view, each numpy arrays.
        # One is your own hidden board while the other is your public board.
        # You will arrange ships on your own hidden board while you will attack your enemies public board.
        
        # You can define a ship with three parameters, a coordinate, a length, and a direction
        # coordinate is a tuple defining the cell with least column or row
        # length is the length of the ship
        # direction defines whether the ship fits within a single row (ROWWISE) or a column (COLUMNWISE)

        #for demonstrations sake lets add this variable
        self.i = 0

        ship = Ship((0,0), 5, COLUMNWISE)  # instantiates our ship
        self.current_game.place_ship(self, ship) #adds our ship

        # if a ship is illegal (out of bounds or overlaps with another ship, place_ship will return false, otherwise it will return true)
        ROWWISE
        COLUMNWISE

        # lets add a few more
        self.current_game.place_ship(self, Ship((0,1), 4, COLUMNWISE))
        self.current_game.place_ship(self, Ship((0,2), 3, COLUMNWISE))
        self.current_game.place_ship(self, Ship((0,3), 3, COLUMNWISE))
        self.current_game.place_ship(self, Ship((7,7), 2, ROWWISE))
        
        #in your bot you will likely need to know how many ships you have, 
        # use the view_ships method to view your existing ships.

        self.current_game.view_ships(self)

        # to view your own board, use view_own_board

        self.current_game.view_own_board(self)


        # the numpy array describes the ships in terms of these constants

        EMPTY # no ship at the position
        SHIP # ship at the position
        
        # some extra constants

        FLEET_TEMPLATE # a tuple of numbers describing what types of ships you should have — (5, 4, 3, 3, 2)
        BOARD_SHAPE # a describes the dimensions of the board — (10, 10)
        

    def play(self):

        # the play method is called every turn. This is where you decide to hit. 
        # if you try to shoot multiple times or none at all you immediately lose
        
        # you can view your enemies board with shoot_enemy, it returns a numpy array
        self.current_game.view_enemy_board(self)

        #like your own board, it also uses constants
        EMPTY #not hit,
        MISS #hit but no ship there
        HIT #hit a ship, but the whole ship is not yet sunk
        SUNKEN #the ship has been completely sunken

        #I know that their is no sunken peg in real battle ship but you would normally say
        # to the opposing player "You sunk my battle ship!" Representing this would be needlessly tedious

        # to shoot your enemy you need to use the shoot_enemy method
        self.current_game.shoot_enemy(self, (self.i//10, self.i%10))
        self.i += 1

        # it will return a boolean whether the shot was illegal. if true, the shot was legal. 
        # However, to know its effects, you will need to use view_enemy_board next turn


if __name__ == "__main__":
    
    # We can easily play vs our two AIS to get a winner

    p1 = Player() #default (completely random player)
    p2 = TemplatePlayer() # our template
    g = Game(p1, p2)  # our game
    g.setup() # allow them to set up
    w = g.play() #make them play, finding a winner
    print(type(w).__name__) # printing the winner

    # # and they can play another time too
    g = Game(p1, p2)
    g.setup() 
    w = g.play()
    print(type(w).__name__)

    # we can run this a 1000 times with compare_accuracy, printing the results
    # compare_accuracy(p1, p2, 10000)
    print_accuracy(p1, p2, 1000)
    graph_accuracy(p1, p2, 100, 10) # this way you can see if your strategy improves over time

    # we can also find a graph of their wins separated into periods

    # we can also show a game using VisibleGame instead of Game
    #however, you must also pass into the constructor the amount of milliseconds each turn should take

    g = VisibleGame(p1, p2, 100)
    g.setup() 
    w = g.play()







    


        
        

