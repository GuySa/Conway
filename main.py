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
        
        # Initializing the board with size BOARD_SIZE+2 by BOARD_SIZE+2.
        # The +2 part puts a boundary around the board to make checking neighbors less exception-inducing
        self.actualBoard = [[0 for _ in range(BOARD_SIZE + 2)] for _ in range(BOARD_SIZE + 2)]

    def build(self):
        for x in range(BOARD_SIZE + 2):
            for y in range(BOARD_SIZE + 2):
                currentCell = Cell(position=(x,y), on_press=self.pressCell)
                self.actualBoard[x][y] = currentCell

                # add the cell to the board only if it isn't the boundary
                if (x != 0) and (x != BOARD_SIZE + 2) and (y != 0) and (y != BOARD_SIZE + 2):
                    self.boardLayout.add_widget(currentCell)

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
        neighborOffsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        currentCount = 0
        currentX, currentY = cellPosition

        for offsetX, offsetY in neighborOffsets:
            if self.actualBoard[currentX-offsetX][currentY-offsetY].background_color ==  LIVE_COLOR:
                currentCount = currentCount + 1

        return currentCount

Conway().run()
