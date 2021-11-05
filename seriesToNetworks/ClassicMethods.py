import numpy as np
import dtw as DTW
import random
import matplotlib.pyplot as plt

class ClassicMethods:

    @staticmethod
    def calcDTW(x1, x2):
        alignment = DTW.dtw(x1, x2, keep_internals=False);
        #alignment.plot(type="threeway")
    
        #DTW.dtw(x1, x2, keep_internals=True, 
        #   step_pattern=DTW.rabinerJuangStepPattern(6, "c"))\
        #   .plot(type="twoway",offset=-2)

        return alignment.distance

    @staticmethod
    def statisticalSignificance(s1, s2):
        values = [];
        shuffled = s2;

        for i in range(1000):
            random.shuffle(shuffled);
            values.append(ClassicMethods.calcDTW(s1, shuffled));

        heights, bins = np.histogram(values, bins=50)
        heights = heights/sum(heights)
        
        bin_centers = 0.5*(bins[1:] + bins[:-1])
        bin_widths = np.diff(bins)

        print(bin_centers);
        print(bin_widths)

        plt.bar(bin_centers, heights, width=bin_widths, color="blue", alpha=0.5)
        plt.show()