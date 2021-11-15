import numpy as np
import matplotlib.pyplot as plot
import random as rnd

from numpy.lib.function_base import copy

class TemporalSerie:
    serieX = []
    serieY = []

    def __init__(self) -> None:
       pass

    def genSineSerie(self, start: int, stop: int, step: int, inc: int =1):
        self.serieX = np.arange(start, stop, step);
        self.serieY = np.sin(self.serieX);
        self.serieY = self.serieY + inc;
        self.serieY = self.serieY / 10;

        return self.serieY;

    def genRandonSerie(self, start:int, stop:int, step:int):
        self.serieX = np.arange(start, stop, step);
        self.serieY = np.random.rand(len(self.serieX))

    def addNoise(self, value):
        newY = copy(self.serieY);

        for i in range(len(self.serieX)):
            newY[i] += rnd.uniform(-value, value)

        return self.serieX, newY;

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