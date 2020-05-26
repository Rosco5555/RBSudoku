import numpy
import pygame
import sys
import copy
from copy import deepcopy
from pygame.locals import *
from board import Board
from board import Cube
from collections import Counter
import copy
from collections import Counter
from generate import Generate



#PYGAME
pygame.init()
pygame.display.set_caption("RBSudoku")
fps = 60
fpsClock = pygame.time.Clock()
width, height = 720, 540
boardDimensions = 360
screen = pygame.display.set_mode((width, height))
cellSize = 40
offsetX = 100
offsetY = 100
font = pygame.font.SysFont('comicsansms', 30)
#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREY = (113, 126, 142)

#Gets grid cordinates from click position

def getCoords(pos):
    x = (pos[0] - offsetX) // (cellSize)
    y = (pos[1] - cellSize) // cellSize
    if 0 <= x <= 9 and 0 <= y <= 9:

        return (x,y)
    else:
        return None
# Game loop.


def main(board):
    origBoard = deepcopy(board)
    errors = 0

    boardObj = Board(board, boardDimensions, boardDimensions, 9, 9, screen, errors)

    #Creating a solve button

    solveButton = pygame.Rect(width - 200, height//2 - 200, 150, 50)
    solveButtonText = font.render("Solve", False, BLACK)

    #Reset Button
    resetButton = pygame.Rect(width - 200, height//2 - 80, 150, 50)
    resetButtonText = font.render("Reset", False, BLACK)

    solved = False
    prevCoords = []


    initBoard = boardObj.board
    #Need the solved state so we can check temp values
    boardObj.solve(initBoard)

    #Start the timer
    elapsed = 0
    timer_started = True
    startTime = pygame.time.get_ticks()

    #Time label
    timeBox = pygame.Rect(width - 200, height//2 + 100, 150, 50)

    #A box for the timer
    timerBox = pygame.Rect(width - 200, height//2 + 150 , 150, 50)

    #Label for errors
    errorBox = pygame.Rect(width - 500, height//2 + 170, 150, 50)

    #menuButton

    menuButton = pygame.Rect(width - 200, height//2 + 20 , 150, 50)
    menuButtonText = font.render("Menu", False, BLACK)

    while True:


      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()


        selectedSquare = boardObj.getSelectedSquare()
        if selectedSquare is not False: #If a square is selected


            cube = boardObj.cubes[selectedSquare[0]][selectedSquare[1]]

            if event.type == pygame.KEYDOWN:

                if event.key == K_0:
                     cube.tempVal = 0

                if event.key == K_1:
                     cube.tempVal = 1
                if event.key == K_2:
                     cube.tempVal = 2
                if event.key == K_3:
                     cube.tempVal = 3

                if event.key == K_4:
                     cube.tempVal = 4

                if event.key == K_5:
                     cube.tempVal = 5
                if event.key == K_6:
                     cube.tempVal = 6

                if event.key == K_7:
                     cube.tempVal = 7

                if event.key == K_8:
                     cube.tempVal = 8

                if event.key == K_9:
                     cube.tempVal = 9

                #If the user presses enter they are trying to enter a value
                if event.key == K_RETURN:
                    cube.enterPressed = True



        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos


            if solveButton.collidepoint(pos):

                boardObj.updateSolve() # This is when the board state should be equal to the solved state we want to display the solved board

            if resetButton.collidepoint(pos):
                main(origBoard)

            if menuButton.collidepoint(pos):
                menu()
            #Have we clicked on a square?
            coords = getCoords(pos)
            #Are we selecting a new square

            if (coords):

                if (prevCoords):
                    boardObj.cubes[prevCoords[0]][prevCoords[1]].selected = False
                    boardObj.cubes[coords[0]][coords[1]].selected = True
                else:
                    boardObj.cubes[coords[0]][coords[1]].selected = True

            prevCoords = coords


      # Update.
      elapsed = pygame.time.get_ticks() - startTime



      # Drawing
      boardObj.drawBoard()

      #Drawing buttons
      pygame.draw.rect(screen, [255, 0, 0], solveButton)
      screen.blit(solveButtonText, (solveButton.left + 30, solveButton.top + 10))

      pygame.draw.rect(screen, [255, 0, 0], resetButton)
      screen.blit(resetButtonText, (resetButton.left + 30, resetButton.top + 10))

      #Time label
      timeText = font.render("Time", True, BLACK)
      screen.blit(timeText, (timeBox.left + 30, timeBox.top + 10))

      #Drawing timer
      if not boardObj.solved:
          pygame.draw.rect(screen, [255, 0, 0], timerBox, 2)

          seconds = elapsed // 1000
          minutes = seconds // 60
          if seconds >= 60:
              seconds = seconds -(minutes * 60)

          timerTextStr = "%d : %d" % (minutes, seconds)

      timerText = font.render(timerTextStr, True, BLACK)
      screen.blit(timerText, (timerBox.left + 30, timerBox.top + 10))

      #Drawing errors




      if boardObj.errors >= 3:
          errorText = font.render("You failed", True, BLACK)
          screen.blit(errorText, (errorBox.left, errorBox.top))
          boardObj.updateSolve()
      else:
           errorTextStr = "Errors: %d" % boardObj.errors
           errorText = font.render(errorTextStr, True, BLACK)
           screen.blit(errorText, (errorBox.left, errorBox.top))


      pygame.draw.rect(screen, [255, 0, 0], menuButton)
      screen.blit(menuButtonText, (menuButton.left + 30, menuButton.top + 10))

      pygame.display.update()
      fpsClock.tick(30)






def menu():

  #EasyButton
  easyButton = pygame.Rect(width - 450, height//2 - 200, 150, 50)
  easyButtonText = font.render("Easy", False, BLACK)

  #mediumButton
  mediumButton = pygame.Rect(width - 450, height//2 - 80, 150, 50)
  mediumButtonText = font.render("Medium", False, BLACK)

  #hardButton
  hardButton = pygame.Rect(width - 450, height//2 + 50 , 150, 50)
  hardButtonText = font.render("Hard", False, BLACK)


  running = True

  while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()
        #When the user clicks on a button a game is started with the corresponding difficulty
        if event.type == pygame.MOUSEBUTTONDOWN:
              pos = event.pos


              if easyButton.collidepoint(pos):
                main(Generate.createSudoku("easy"))


              if mediumButton.collidepoint(pos):
                  main(Generate.createSudoku("medium"))

              if hardButton.collidepoint(pos):
                main(Generate.createSudoku("hard"))
      #drawing
      screen.fill(GREY)

      #Drawing buttons
      #Drawing buttons
      pygame.draw.rect(screen, [255, 0, 0], easyButton)
      screen.blit(easyButtonText, (easyButton.left + 30, easyButton.top + 10))

      pygame.draw.rect(screen, [255, 0, 0], mediumButton)
      screen.blit(mediumButtonText, (mediumButton.left + 30, mediumButton.top + 10))

      pygame.draw.rect(screen, [255, 0, 0], hardButton)
      screen.blit(hardButtonText, (hardButton.left + 30, hardButton.top + 10))


      #Update
      pygame.display.update()

menu()
