import numpy as np
import dtw as DTW
import random
import matplotlib.pyplot as plot

class ClassicMethods:

    @staticmethod
    def calcDTW(x1, x2, plotResult):
        alignment = DTW.dtw(x1, x2, keep_internals=True if plotResult else False);
    
        if(plotResult):
            alignment.plot(type="threeway")
            DTW.dtw(x1, x2, keep_internals=True, 
            step_pattern=DTW.rabinerJuangStepPattern(6, "c"))\
            .plot(type="twoway",offset=-2)

        return alignment.distance

    @staticmethod
    def statisticalSignificance(s1, s2):
        values = [];
    
        shuffled1 = s1;
        shuffled2 = s2;

        for i in range(1000):
            random.shuffle(shuffled1);
            random.shuffle(shuffled2);
            values.append(ClassicMethods.calcDTW(shuffled1, shuffled2, False));

        heights, bins = np.histogram(values, bins=50)
        heights = heights/sum(heights)
        
        bin_centers = 0.5*(bins[1:] + bins[:-1])
        bin_widths = np.diff(bins)

        plot.bar(bin_centers, heights, width=bin_widths, color="blue", alpha=0.5)
        print(values)
        plot.show()

    @staticmethod
    def plotSeries(sx, sy) -> None:
        plot.plot(sx, sy)
        plot.title('Sine wave')
        plot.xlabel('Time')
        plot.ylabel('Amplitude = sin(time)')
        plot.grid(True, which='both')
        plot.axhline(y=0, color='k')
        plot.show()