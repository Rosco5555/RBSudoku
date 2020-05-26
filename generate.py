#Generation of sudoku boards
import numpy
import random
import copy
from copy import deepcopy
class Generate:

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



    def solve(board):


        emptySquare = Generate.getEmptySquare(board)
        #If there are no empty squares we are done
        if  not emptySquare:

            return board
        else:


            row = emptySquare[0]
            col = emptySquare[1]


        for n in range(1,10):
            #Trying to insert a value into the empty square
            if Generate.canInsert(row, col, n, board):

                board[row][col] = n
                #Do this for another square
                if Generate.solve(board):
                    return True
                #If we can't them we have made a wrong decision somewhere it's time to back track
                board[row][col] = 0

        return False

    def fillBoard(grid):

        #Lets randomly insert 3-12 numbers into random positions
        i = random.randint(3,15)
        for x in range(i):
            run = True
            while run:


                value = random.randint(1,9)
                x =  random.randint(0,8)
                y =  random.randint(0,8)

                #Try inserting this value

                if Generate.canInsert(y, x, value, grid):
                    grid[y][x] = value
                    run = False
        return grid

        #Need to keep doing this until we have a fully solved board

    def fillWithNums():
        solved = False
        attempts = 0
        while not solved and attempts < 10:

            grid = [[0]*9 for i in range(9)]
            Generate.fillBoard(grid)

            if Generate.solve(grid) != False:
                solved = True
                return Generate.solve(grid)
            else:
                attempts += 1

    def createSudoku(difficulty):
        n = 0
        toRemove = 0
        if difficulty == "easy":
            n = random.randint(36,40)
            toRemove = abs(n-81)

        if difficulty == "medium":
            n = random.randint(27,36)
            toRemove = abs(n-81)
        if difficulty == "hard":
            n = random.randint(19,26)
            toRemove = abs(n-81)


        grid = Generate.fillWithNums()


        for i in range(toRemove):

            y = random.randint(0,8)
            x = random.randint(0,8)
            value = grid[y][x]
            #Removing the value



            grid[y][x] = 0


            gridCopy = deepcopy(grid)
            gridCopy2 = deepcopy(grid)

            g1 = Generate.solve(gridCopy)
            g2 = Generate.solve(gridCopy2)




            #If the solution is not unique or the grid is now unsolvable we should put the value back

            if g1 != g2 or g1 == False:
                grid[y][x] = value

        return grid
