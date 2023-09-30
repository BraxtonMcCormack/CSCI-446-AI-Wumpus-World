class StatisticTracker:
    def __init__(self):
        self.points = 10000     #Initial points
        self.actionCost = 1     #The cost of one action
        self.goldCost = 1000    #The reward of finding gold
        self.deathCost = 10000  #The cost of one death
    '''Returns points'''
    def getPoints(self):
        return self.points
    '''Helper Functions to change cost'''
    def costAction(self):
        self.points -= self.actionCost
    def costGold(self):
        self.points += self.goldCost
    def costDeath(self):
        self.points -= self.deathCost
