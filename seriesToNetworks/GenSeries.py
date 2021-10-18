import numpy as np
import matplotlib.pyplot as plot

class GenSeries:
    def __init__(self) -> None:
       pass

    def SineSerie(self, start: int, stop: int, step: int) -> bool:
        x = np.arange(start, stop, step);
        y = np.sin(x);
        y = y+1
        y = y/10
        toFile(x, y);
        
        plot.plot(x, y)
        plot.title('Sine wave')
        plot.xlabel('Time')
        plot.ylabel('Amplitude = sin(time)')
        plot.grid(True, which='both')
        plot.axhline(y=0, color='k')
        plot.show()

        return True;

def toFile(time, amplitude) -> None:
    f = open("timeSeries.txt", "w+");
    for i in range(len(time)):
        f.write(f"{round(time[i], 1)}\t{round(amplitude[i], 3)}\n");