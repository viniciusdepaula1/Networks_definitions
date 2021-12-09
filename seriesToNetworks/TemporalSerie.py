import numpy as np
import matplotlib.pyplot as plot
import random as rnd

from numpy.lib.function_base import copy

class TemporalSerie:
    serieX = []
    serieY = []
    casasDecimais = 8

    def __init__(self) -> None:
       pass

    def genSineSerie(self, start: int, stop: int, step: int, inc: int =1):
        self.serieX = np.arange(start, stop, step);
        self.serieY = np.sin(self.serieX);
        self.serieY = self.serieY + inc;
        self.serieY = self.serieY / 10; # ((sen x) + 5)/ 10 

        #self.serieY = [round(num, self.casasDecimais) for num in self.serieY];

        return self.serieY;

    def genRandonSerie(self, start:int, stop:int, step:int):
        self.serieX = np.arange(start, stop, step);
        self.serieY = np.random.rand(len(self.serieX))

    def addNoise(self, value):
        newY = copy(self.serieY);

        for i in range(len(self.serieX)):
            newY[i] += rnd.uniform(-value, value)

        #newY = [round(num, self.casasDecimais) for num in newY];

        return self.serieX, newY;

    def addNoiseInt(self, y, value):
        newY = copy(y);

        for i in range(len(y)):
            newY[i] += (rnd.randint(-1, 1))

        return newY;

    def minMaxScaling(self):
        newY = copy(self.serieY);
        newY = np.array(newY)
        newY = 1 + (((newY - newY.min()) * (10000 - 1)) / newY.max() - newY.min())
        newY = newY + 3250;
        newY = [int(num) for num in newY]
        return newY

    def plotSeries(self) -> None:
        plot.plot(self.serieX, self.serieY)
        plot.title('Sine wave')
        plot.xlabel('Time')
        plot.ylabel('Amplitude = sin(time)')
        plot.grid(True, which='both')
        plot.axhline(y=0, color='k')
        plot.show()

    def toFile(self, fileName) -> None:
        f = open(fileName, "w+");
        for i in range(len(self.serieX)):
            f.write(f"{round(self.serieX[i], 1)}\t{round(self.serieY[i], 3)}\n");