from sympy.integrals.risch import NonElementaryIntegral


class Location(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, delta_x, delta_y):
        return Location(self.x + delta_x, self.y + delta_y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def dist_from(self, other):
        xDist = self.x - other.getX()
        yDist = self.y - other.getY()

        return (xDist**2 + yDist **2)**0.5

    def __str__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'

class Drunk(object):
    def __init__(self, name = None):
        self.name = name

    def __str__ (self):
        if self != None:
            return self.name
        return 'Anonymous'


import random

class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0.1), (0,-1), (1,0), (-1,0)]
        return random.choice(stepChoices)

class MasochistDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0.0, 1.1), (0.0, -0.9), (1.0, 0.0), (-1.0, 0.0)]

        return random.choice(stepChoices)

class Field(object):
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')

        else:
            self.drunks[drunk] = loc


    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')

        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        self.drunks[drunk] = currentLocation.move(xDist, yDist)














