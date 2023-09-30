class Agent:
    def __init__(self):
        self.percSmell = False
        self.percBreeze = False
        self.Glitter = False
        self.percWall = False
        self.percScream = False
        self.curLocation = (0,0)
        self.numArrows = 1
    def up(self):
        self.curLocation = (self.curLocation[0],self.curLocation[1]+1)
    def down(self):
        self.curLocation = (self.curLocation[0], self.curLocation[1]-1)
    def left(self):
        self.curLocation = (self.curLocation[0]-1, self.curLocation[1])
    def right(self):
        self.curLocation = (self.curLocation[0]+1, self.curLocation[1])

    def shoot(self, direction):
        if self.numArrows >0:
            #fireArrow(direction)
            self.numArrows -= 1
        else:
            print("No arrows left")
        pass

    def setNumArrows(self, num):
        self.numArrows = num






