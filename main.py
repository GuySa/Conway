import time

try:
    from kivy.uix.gridlayout import GridLayout
    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.clock import Clock
except ImportError:
    print "Error importing Kivy. are you sure you have Kivy installed?"
    raise SystemExit(1)

BOARD_SIZE = 18
LIVE_COLOR = [1,1,1,1]
DEAD_COLOR = [0.1,0.1,0.1,1]
SLEEP_BETWEEN_STEPS = 0.5

class Cell(Button):
    def __init__(self, position, **kwargs):
        super(Button, self).__init__(background_normal="", background_color=DEAD_COLOR, **kwargs)
        self.position = position
        self.cellState = "dead"

    def death(self):
        self.cellState = "dead"
        self.background_color = DEAD_COLOR

    def birth(self):
        self.cellState = "alive"
        self.background_color = LIVE_COLOR

    def switchState(self):
        if self.cellState is "alive":
            self.death()
        elif self.cellState is "dead":
            self.birth()
        else:
            raise Exception("Cell not alive nor dead!")

class Conway(App):
    def __init__(self):
        App.__init__(self)
        self.numOfSteps = 0
        self.isGameRunning = False
        self.boardLayout = GridLayout(cols=BOARD_SIZE)
        
        # Initializing the board with size BOARD_SIZE by BOARD_SIZE
        self.actualBoard = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def build(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                currentCell = Cell(position=(x,y), on_press=self.pressCell)
                self.boardLayout.add_widget(currentCell)
                self.actualBoard[x][y] = currentCell

        self.boardLayout.add_widget(Button(text="Step!", on_press=self.oneStep))
        self.boardLayout.add_widget(Button(text="Run!", on_press=self.runGame))

        return self.boardLayout

    def pressCell(self, instance):
        instance.switchState()

    def oneStep(self, instance):
        # This will be a list of tuples which denote the coordinates of cell that need to switch state
        changes = []

        # Going through every cell and checking death/birth
        for currentRow in self.actualBoard:
            for currentCell in currentRow:
                numOfLivingNeighbors = self.NumberOfLivingNeighbors(currentCell.position)

                if currentCell.cellState is "alive":
                    # Check death by loneliness
                    if numOfLivingNeighbors <= 1:
                        changes.append(currentCell.position)

                    # Check death by over-population
                    if numOfLivingNeighbors > 3:
                        changes.append(currentCell.position)

                elif currentCell.cellState is "dead":
                    # Check birth
                    if numOfLivingNeighbors == 3:
                        changes.append(currentCell.position)

                else:
                    raise Exception("Cell not alive nor dead!")

        # Making changes
        for x,y in changes:
            self.actualBoard[x][y].switchState()

        print "Finished Step #{}".format(self.numOfSteps)
        self.numOfSteps = self.numOfSteps + 1

        return self.isGameRunning

    def runGame(self, instance):
        if self.isGameRunning is False:
            self.isGameRunning = True
            instance.text = "Stop!"
            Clock.schedule_interval(self.oneStep, SLEEP_BETWEEN_STEPS)

        else:
            self.isGameRunning = False
            instance.text = "Run!"

    def NumberOfLivingNeighbors(self, cellPosition):
        currentCount = 0
        currentX, currentY = cellPosition

        # Going through the column to the left of the current cell
        if currentX - 1 >= 0:
            if currentY - 1 >= 0:
                if self.actualBoard[currentX-1][currentY-1].background_color ==  LIVE_COLOR:
                    currentCount = currentCount + 1

            if self.actualBoard[currentX-1][currentY].background_color ==  LIVE_COLOR:
                currentCount = currentCount + 1

            if currentY + 1 < BOARD_SIZE:
                if self.actualBoard[currentX-1][currentY+1].background_color ==  LIVE_COLOR:
                    currentCount = currentCount + 1

        # Going through the current cell's column
        if currentY - 1 >= 0:
            if self.actualBoard[currentX][currentY-1].background_color ==  LIVE_COLOR:
                currentCount = currentCount + 1

        if currentY + 1 < BOARD_SIZE:
            if self.actualBoard[currentX][currentY+1].background_color ==  LIVE_COLOR:
                currentCount = currentCount + 1

        # Going through the column to the right of the current cell
        if currentX + 1 < BOARD_SIZE:
            if currentY - 1 >= 0:
                if self.actualBoard[currentX+1][currentY-1].background_color ==  LIVE_COLOR:
                    currentCount = currentCount + 1

            if self.actualBoard[currentX+1][currentY].background_color ==  LIVE_COLOR:
                currentCount = currentCount + 1

            if currentY + 1 < BOARD_SIZE:
                if self.actualBoard[currentX+1][currentY+1].background_color ==  LIVE_COLOR:
                    currentCount = currentCount + 1

        return currentCount

Conway().run()
