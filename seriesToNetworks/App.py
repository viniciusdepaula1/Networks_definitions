import TemporalSerie as TS
from ClassicMethods import *
from DCTIF import *
from DCSD import *
from VG import *

def testeSin():
    serie1 = TS.TemporalSerie();
    serie2 = TS.TemporalSerie();

    serie1.genSineSerie(0, 10, 0.1);
    serie2.genSineSerie(0, 10, 0.1);

    serie2.addNoise(range(10, 20), 0.01);

    #serie1.toFile("timeSerie1.txt");
    #serie2.toFile("timeSerie2.txt");

    #serie1.plotSeries();
    #serie2.plotSeries();
        
    #graphSin1 = DCTIF("timeSerie1.txt");
    #graphSin2 = DCSD("timeSerie1.txt");
    #graphSin3 = VG("timeSerie1.txt");

    #graphSinNoise1 = DCTIF("timeSerie2.txt");
    #graphSinNoise2 = DCSD("timeSerie2.txt");
    #graphSinNoise3 = VG("timeSerie2.txt");

def testeRand():
    serie3 = TS.TemporalSerie();

    serie3.genRandonSerie(0, 10, 0.1);

    #serie3.toFile("timeSeriesRand.txt");
    
    serie3.plotSeries();

    #graphRand1 = DCTIF("timeSeriesRand.txt");
    #graphRand2 = DCSD("timeSeriesRand.txt");
    #graphRand3 = VG("timeSeriesRand.txt");

def main():
    #dtwAlignment = ClassicMethods.calcDTW(x1, x2);
    
    #print (dtwAlignment);
    
    #ClassicMethods.statisticalSignificance(x1, x2);

    pass

if __name__ == "__main__":
    main()