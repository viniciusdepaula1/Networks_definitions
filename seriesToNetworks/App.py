import TemporalSerie as TS
from ClassicMethods import *
from DCTIF import *
from DCSD import *
from VG import *

def main():
    serie1 = TS.TemporalSerie();
    serie2 = TS.TemporalSerie();

    x1 = serie1.GenSineSerie(0, 10, 0.1);
    x2 = serie2.GenSineSerie(0, 10, 0.1);

    serie2.addNoisy(range(10, 20), 0.01);

    serie1.toFile("timeSerie1.txt");
    serie2.toFile("timeSerie2.txt");

    serie1.plotSeries();
    serie2.plotSeries();

    dtwAlignment = ClassicMethods.calcDTW(x1, x2);
    print (dtwAlignment);
    
    graph1 = DCTIF("timeSerie1.txt");
    graph2 = DCSD("timeSerie1.txt");
    graph3 = VG("timeSerie1.txt");

    graph11 = DCTIF("timeSerie2.txt");
    graph22 = DCSD("timeSerie2.txt");
    graph33 = VG("timeSerie2.txt");

    pass

if __name__ == "__main__":
    main()