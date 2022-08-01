# Neuron Object - Represents and Individual SUPG

from mimetypes import init

from zmq import NULL


class sNeuron(object):
    
    def __init__(self, neuronID):
        self.neuronID = neuronID
        self.xPos = 0
        self.yPos = 0
        self.timeCounter = 0
        self.firstStepComplete = False

    def ID(self):    
        return self.neuronID

    def getXPos(self):
        return self.xPos
    
    def getYPos(self):
        return self.yPos

    def getFirstStepComplete(self):
        return self.firstStepComplete
    
    def setStepComplete(self):
        self.firstStepComplete = True

    def setXPos(self, x):
        self.xPos = x

    def setYPos(self, y):
        self.yPos = y

    def getTimeCounter(self):
        return self.timeCounter

    def setTimeCounter(self, val):
        self.timeCounter = val

    def updateT(self):
        self.timeCounter = (self.timeCounter + 1) % 100