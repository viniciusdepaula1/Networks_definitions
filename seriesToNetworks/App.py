from numpy.lib.function_base import copy
import TemporalSerie as TS
from ClassicMethods import *
from DCTIF import *
from DCSD import *
from VG import *
import matplotlib.pyplot as plot
import pandas as pd
import csv
import seaborn as sns

# ruido em uma freq (gaussiana)
# distribuíção uniforme
# intensidade (de 0 até 1 vezes a intenção)

#caotico + periódico

# pega uma métrica (dtw) altera os valores de i
# e ve oq q da a forma da curva
# para cada i 1000 séries.
# envelope -- resultados possíveis para cada i
# boxplot para cada i

def plotDtwResults():
    gapminder = pd.read_csv('dtwResults.csv');
    print(gapminder.Distance[0])
    my_dict = {'0.05': gapminder.Distance[0:1000], '0.1': gapminder.Distance[1000:2000],
                '0.15': gapminder.Distance[2000:3000], '0.2':gapminder.Distance[3000:4000],
                '0.25': gapminder.Distance[4000:5000], '0.3':gapminder.Distance[6000:7000],
                '0.4': gapminder.Distance[7000:8000]}
    
    fig, ax = plot.subplots()
    ax.boxplot(my_dict.values())
    ax.set_xticklabels(my_dict.keys())
    plot.xlabel('Intensity')
    plot.ylabel('Distance')
    plot.show()


def calcI(serie1, serie2, iValues, dtwResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    s2X, s2Y = serie2.addNoise(iValue)

    dtwAlignment = ClassicMethods.calcDTW(s1Y, s2Y, False)

    iValues.append(iValue)
    dtwResults.append(dtwAlignment)

def similaridadexintensidade():
    serie1 = TS.TemporalSerie()
    serie2 = TS.TemporalSerie()

    iValues = []
    dtwResults = []

    iValue = 0.05  # 0.05 até 0.40 == 8 iterações == 8000 testes

    serie1.genSineSerie(0, 20, 0.1, 5)
    serie2.genSineSerie(0, 20, 0.1, 5)

    for i in range(1000):
        calcI(serie1, serie2, iValues, dtwResults, iValue)

    iValue = 0.1

    for i in range(1000):
        calcI(serie1, serie2, iValues, dtwResults, iValue)

    iValue = 0.15

    for i in range(1000):
        calcI(serie1, serie2, iValues, dtwResults, iValue)

    iValue = 0.2

    for i in range(1000):
        calcI(serie1, serie2, iValues, dtwResults, iValue)

    iValue = 0.25

    for i in range(1000):
        calcI(serie1, serie2, iValues, dtwResults, iValue)

    iValue = 0.3

    for i in range(1000):
        calcI(serie1, serie2, iValues, dtwResults, iValue)

    iValue = 0.35

    for i in range(1000):
        calcI(serie1, serie2, iValues, dtwResults, iValue)

    iValue = 0.4

    for i in range(1000):
        calcI(serie1, serie2, iValues, dtwResults, iValue)

    f = open("dtwResults.csv", "w+");
    writer = csv.writer(f);
    header = ['Intensity', 'Distance']
    writer.writerow(header)

    for i in range(len(iValues)):
        data = [iValues[i], dtwResults[i]];
        writer.writerow(data);

def testeSin():
    serie1 = TS.TemporalSerie()
    serie2 = TS.TemporalSerie()

    serie1.genSineSerie(0, 10, 0.1)
    serie2.genSineSerie(0, 10, 0.1)

    serie2.addNoise(0.1)

    # serie1.toFile("timeSerie1.txt");
    # serie2.toFile("timeSerie2.txt");

    serie1.plotSeries()
    serie2.plotSeries()

    #graphSin1 = DCTIF("timeSerie1.txt");
    #graphSin2 = DCSD("timeSerie1.txt");
    #graphSin3 = VG("timeSerie1.txt");

    #graphSinNoise1 = DCTIF("timeSerie2.txt");
    #graphSinNoise2 = DCSD("timeSerie2.txt");
    #graphSinNoise3 = VG("timeSerie2.txt");

    dtwAlignment = ClassicMethods.calcDTW(serie1.serieY, serie2.serieY, True)
    print(dtwAlignment)


def testeRand():
    serie3 = TS.TemporalSerie()

    serie3.genRandonSerie(0, 10, 0.1)

    # serie3.toFile("timeSeriesRand.txt");

    serie3.plotSeries()

    #graphRand1 = DCTIF("timeSeriesRand.txt");
    #graphRand2 = DCSD("timeSeriesRand.txt");
    #graphRand3 = VG("timeSeriesRand.txt");


def main():
    #similaridadexintensidade()
    plotDtwResults()
    #dtwAlignment = ClassicMethods.calcDTW(x1, x2);

    #print (dtwAlignment);

    #ClassicMethods.statisticalSignificance(x1, x2);

    pass


if __name__ == "__main__":
    main()
