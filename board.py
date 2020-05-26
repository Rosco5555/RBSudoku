import numpy
import pygame
import sys
from pygame.locals import *
from collections import Counter

#COLORS AND CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0, 50)
MAGENTA = (255, 0 , 144, 100)
GREY = (113, 126, 142)
offsetX = 100
offsetY = 100
cellSize = 40
height = 540


initBoard = [[2,9,0,0,0,0,0,7,0],
       [3,0,6,0,0,8,4,0,0],
       [8,0,0,0,4,0,0,0,2],
       [0,2,0,0,3,1,0,0,7],
       [0,0,0,0,8,0,0,0,0],
       [1,0,0,9,5,0,0,6,0],
       [7,0,0,0,9,0,0,0,1],
       [0,0,1,2,0,0,3,0,6],
       [0,3,0,0,0,0,0,5,9]]

class Board:

    def __init__(self, board, width, height, rows, cols, screen, errors):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[col][row], row, col, width, height, screen, self) for col in range(cols)] for row in range(rows)]
        self.solvedState = None
        self.screen = screen
        self.solved = False
        self.errors = errors
    def setSolvedState(self, state):

        self.solvedState = [[Cube(state[col][row], row, col, self.width, self.height, self.screen, self) for col in range(self.cols)] for row in range(self.rows)]

    def canInsert(y, x, val, board):

        #Checking the value is unique in it's row and column
        for i in range(0,9):
            if board[y][i] == val:
                return False
            if board[i][x] == val:
                return False

        #Which box are we in?
        x0 = (x//3) * 3
        y0 = (y//3) * 3

        for i in range(0,3):
            for j in range(0,3):
                if board[y0 + i][x0 + j] == val:
                    return False
        return True

    def getEmptySquare(board):
        #Are there any empty squares? If so give me the coordinates of the first one we find
        for i in range(0,9):
            for j in range(0,9):
                if board[i][j] == 0:
                    return (i, j)
        return None


    def solve(self,board):

        emptySquare = Board.getEmptySquare(board)
        #If there are no empty squares we are done
        if not emptySquare:
            #Initialising the solved state
            Board.setSolvedState(self, board)
            return True
        else:
            row, col = emptySquare

        for n in range(1,10):
            #Trying to insert a value into the empty square
            if Board.canInsert(row, col, n, board):

                board[row][col] = n
                #Do this for another square
                if Board.solve(self, board):
                    return True
                #If we can't them we have made a wrong decision somewhere it's time to back track
                board[row][col] = 0

        return False

    def updateSolve(self):
        #want all the cubes to have the values as the boardstate
         self.cubes = self.solvedState
         self.solved = True

    def isSolved(self):

        if self.cubes == self.solvedState:
            self.solved = True
            return True
        return False



    def drawBoard(self):
        self.screen.fill(WHITE)
        #Start by drawing the lines

        #draw 9 vertical lines
        for x in range(1, 10):
            #Every 3rd line is dark
            if (x % 3 == 0):
                pygame.draw.line(self.screen, BLACK, (offsetX + x*cellSize, cellSize), (offsetX + x*cellSize, cellSize + ( self.width) ), 3)
            else:
                pygame.draw.line(self.screen, BLACK, (offsetX + x*cellSize, cellSize), (offsetX + x*cellSize,  cellSize + ( self.width) ))

        #drawing 9 horizontal lines
        for y in range(0,10):
            #Every 3rd line is dark
            if (y % 3 == 0):

                pygame.draw.line(self.screen, BLACK, (offsetX,  (cellSize) + (y * cellSize) ), (offsetX + (9 * cellSize),  (cellSize)  + (y * cellSize)), 3 )
            else:
                pygame.draw.line(self.screen, BLACK, (offsetX,  (cellSize) + (y * cellSize) ), (offsetX + (9 * cellSize),  (cellSize)  + (y * cellSize)))

        #Drawing a rectangle around the board?
        pygame.draw.rect(self.screen, BLACK, (offsetX, cellSize, (self.width), height - offsetY - ( 2* cellSize) ), 5)

        #drawing the cubes
        for row in range(self.rows):
            for col in range(self.cols):
                self.cubes[row][col].drawCube()

    #Function that returns the selected square
    def getSelectedSquare(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cubes[row][col].selected:
                    return (row, col)
        return False






class Cube:

    def __init__(self, value, row, col, width, height, screen, board):
        self.value = value
        self.row = row
        self.col = col
        self.selected = False
        self.width = width
        self.height = height
        self.screen = screen
        self.tempVal = 0
        self.Clicked = False
        self.x = (self.col+1) * cellSize
        self.y = offsetX + (self.row * cellSize)
        self.board = board
        self.enterPressed = False

    def drawCube(self):
        font1 = pygame.font.Font('freesansbold.ttf', 15)
        font2 = pygame.font.Font('freesansbold.ttf', 10)
        #If the square is selected let's highlight it green
        if self.selected and not self.enterPressed:
            self.highlight(GREEN)
        #If the square is selected and the user has pressed enter they are trying to enter a value
        if self.selected and self.enterPressed:

            if self.isCorrectValue():

                self.value = self.tempVal
                self.tempVal = 0
                self.enterPressed = False
                self.selected = False

                #Also need to check if we just put in the last correct value thus solving the soduku
                self.board.isSolved()


            #If it is incorrect don't allow the user to enter it and highlight the square
            else:
                self.board.errors += 1
                print(self.board.errors)
                self.highlight((255,0,0))
                self.enterPressed = False


        # Don't display zeros
        if not (self.value == 0) and self.tempVal == 0:

            text = font1.render(str(self.value), True, BLACK, WHITE)
            textRect = text.get_rect()
            textRect.top = self.x + cellSize//2
            textRect.left = self.y + cellSize//2
            self.screen.blit(text,textRect)

        if not (self.tempVal == 0):
                #Display temp/penciled in values
                text = font2.render(str(self.tempVal), True, GREY)
                textRect = text.get_rect()
                textRect.top = self.x + cellSize//2 - 10
                textRect.left = self.y + cellSize//2 - 10
                self.screen.blit(text,textRect)

    def isCorrectValue(self):

        if (self.tempVal == self.board.solvedState[self.row][self.col].value): #We have the correct value (ASSUMING ONLY ONE UNIQUE SOLUTION)
            return True
        return False

    def highlight(self, color):
        pygame.draw.rect(self.screen, color, (self.y + 1, self.x + 1, cellSize-2, cellSize-2), 2 )
