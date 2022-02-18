
from game import *
import pygame as p
from players import Player
from random import randrange

CELL_DIMENSIONS = 60
GUI_SHAPE = (BOARD_SHAPE[1] * CELL_DIMENSIONS * 2, BOARD_SHAPE[0] * CELL_DIMENSIONS)


def canvas_coords(right, coordinate):
    row, col = coordinate
    x = col * CELL_DIMENSIONS
    y = row * CELL_DIMENSIONS
    extra = GUI_SHAPE[0]/2 if right else 0
    return (x+extra+CELL_DIMENSIONS/2, y+CELL_DIMENSIONS/2)

class VisibleGame(Game):

    def __init__(self, player1, player2, rate):
        super().__init__(player1, player2)
        self.rate = rate
        p.init()
        self._surface = p.display.set_mode(GUI_SHAPE)

        

    def play(self):
        self.setup()
        for i in range(0, 2*BOARD_SHAPE[0]*BOARD_SHAPE[1]):
            p.event.get()
            self._player1.play()
            self.draw()
            p.time.wait(self.rate)
            if self._winner:
                self.review()
                p.time.wait(5000)
                return self._player1
            p.event.get()
            self._player2.play()
            self.draw()
            p.time.wait(self.rate)
            if self._winner:
                self.review()
                p.time.wait(5000)
                return self._player2

    def draw(self):
        self.draw_board()
        self.draw_pegs(1)
        self.draw_pegs(2)
        p.display.update()

    def draw_board(self):

        p.display.set_caption("BATTLESHIP")
        for i in range(0, BOARD_SHAPE[1]*2):
            for j in range(0, BOARD_SHAPE[0]):
                p.draw.rect(self._surface, (255, 255, 255), p.Rect(CELL_DIMENSIONS*i, CELL_DIMENSIONS*j, CELL_DIMENSIONS, CELL_DIMENSIONS), 1)
                p.draw.line(self._surface, (230, 220, 0), (GUI_SHAPE[0]/2, 0), (GUI_SHAPE[0]/2, GUI_SHAPE[1]),5)

    def draw_pegs(self, player_num):
        
        player = self._player2 if player_num == 2 else self._player1

        for i in range(BOARD_SHAPE[0]):
            for j in range(BOARD_SHAPE[1]):
                if self._own_board[player].hidden_arr[i][j] == SHIP:
                    p.draw.circle(self._surface, (200, 200, 190), canvas_coords(player_num == 2, (i,j)), CELL_DIMENSIONS*0.5)
                if self._own_board[player].visible_arr[i][j] == MISS:
                    p.draw.circle(self._surface, (255, 255, 255), canvas_coords(player_num == 2, (i,j)), CELL_DIMENSIONS*0.3)
                elif self._own_board[player].visible_arr[i][j] == HIT:
                    p.draw.circle(self._surface, (200, 0, 0), canvas_coords(player_num == 2, (i,j)), CELL_DIMENSIONS*0.3)
                elif self._own_board[player].visible_arr[i][j] == SUNKEN:
                    p.draw.circle(self._surface, (100, 0, 0), canvas_coords(player_num == 2, (i,j)), CELL_DIMENSIONS*0.5)
