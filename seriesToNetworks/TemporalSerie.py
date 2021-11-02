import numpy as np
import matplotlib.pyplot as plot

class TemporalSerie:
    serieX = []
    serieY = []

    def __init__(self) -> None:
       pass

    def GenSineSerie(self, start: int, stop: int, step: int):
        self.serieX = np.arange(start, stop, step);
        self.serieY = np.sin(self.serieX);
        self.serieY = self.serieY + 1;
        self.serieY = self.serieY / 10;

        return self.serieY;

    def addNoisy(self, rangeValues, value):
        for i in rangeValues:
            self.serieY[i] += value

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