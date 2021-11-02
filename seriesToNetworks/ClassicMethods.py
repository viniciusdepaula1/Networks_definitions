import numpy as np
import dtw as DTW

class ClassicMethods:
    
    @staticmethod
    def calcDTW(x1, x2):
        alignment = DTW.dtw(x1, x2, keep_internals=True);
        alignment.plot(type="threeway")
    
        DTW.dtw(x1, x2, keep_internals=True, 
            step_pattern=DTW.rabinerJuangStepPattern(6, "c"))\
            .plot(type="twoway",offset=-2)

        return alignment.distance

    

