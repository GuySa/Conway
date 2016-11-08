from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button

import copy

# from time import sleep
# import pdb

boardSize = 19
liveColor = [1,1,1,1]
deadColor = [0.1,0.1,0.1,1]

class Cell(Button):
    def __init__(self, position, **kwargs):
        super(Button, self).__init__(background_normal="", background_color=deadColor, **kwargs)
        self.position = position
        self.cellState = "dead"

    def death(self):
        self.cellState = "dead"
        self.background_color = deadColor

    def birth(self):
        self.cellState = "alive"
        self.background_color = liveColor


class Conway(App):
    def __init__(self):
        App.__init__(self)
        self.boardLayout = GridLayout(cols=boardSize)
        
        # Initializing the board with size boardSize by boardSize
        self.actualBoard = [[0 for _ in range(boardSize)] for _ in range(boardSize)]

    def build(self):
        for x in range(boardSize):
            for y in range(boardSize):
                currentCell = Cell(position=(x,y), on_press=self.pressCell)
                self.boardLayout.add_widget(currentCell)
                self.actualBoard[x][y] = currentCell

        self.boardLayout.add_widget(Button(text="Step!", on_press=self.oneStep))

        return self.boardLayout;

    def pressCell(self, instance):
        if instance.background_color == deadColor:
            instance.background_color = liveColor
        else:
            instance.background_color = deadColor

    def oneStep(self, instance):
        # Create a deep copy of the board
        tempBoard = copy.deepcopy(self.actualBoard)

        # Going through every cell and checking death/birth
        for currentRow in self.actualBoard:
            for currentCell in currentRow:
                numOfLivingNeighbors = self.NumberOfLivingNeighbors(currentCell.position)

                if currentCell.cellState == "alive":
                    # Check death by loneliness
                    if numOfLivingNeighbors <= 1:
                        tempBoard[currentCell.position[0]][currentCell.position[1]].death()

                    # Check death by over-population
                    if numOfLivingNeighbors > 3:
                        tempBoard[currentCell.position[0]][currentCell.position[1]].death()

                else:
                    # Check birth
                    if numOfLivingNeighbors == 3:
                        tempBoard[currentCell.position[0]][currentCell.position[1]].birth()

        self.actualBoard = tempBoard


    def NumberOfLivingNeighbors(self, cellPosition):
        currentCount = 0
        currentX, currentY = cellPosition

        # Going through the column to the left of the current cell
        if currentX - 1 >= 0:
            if currentY - 1 >= 0:
                if self.actualBoard[currentX-1][currentY-1].background_color ==  liveColor:
                    currentCount = currentCount + 1

            if self.actualBoard[currentX-1][currentY].background_color ==  liveColor:
                currentCount = currentCount + 1

            if currentY + 1 < boardSize:
                if self.actualBoard[currentX-1][currentY+1].background_color ==  liveColor:
                    currentCount = currentCount + 1

        # Going through the current cell's column
        if currentY - 1 >= 0:
            if self.actualBoard[currentX][currentY-1].background_color ==  liveColor:
                currentCount = currentCount + 1

        if currentY + 1 < boardSize:
            if self.actualBoard[currentX][currentY+1].background_color ==  liveColor:
                currentCount = currentCount + 1

        # Going through the column to the right of the current cell
        if currentX + 1 < boardSize:
            if currentY - 1 >= 0:
                if self.actualBoard[currentX+1][currentY-1].background_color ==  liveColor:
                    currentCount = currentCount + 1

            if self.actualBoard[currentX+1][currentY].background_color ==  liveColor:
                currentCount = currentCount + 1

            if currentY + 1 < boardSize:
                if self.actualBoard[currentX+1][currentY+1].background_color ==  liveColor:
                    currentCount = currentCount + 1

        return currentCount

Conway().run()

