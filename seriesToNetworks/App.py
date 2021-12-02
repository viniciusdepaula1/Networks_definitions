import numpy
from numpy.lib.function_base import copy
import TemporalSerie as TS
from ClassicMethods import *
from DCTIF import *
from DCSD import *
from VG import *
import pandas as pd
import csv
import plotly.express as px
from scipy import stats
import sklearn.metrics as sm

# ruido em uma freq (gaussiana)
# distribuíção uniforme
# intensidade (de 0 até 1 vezes a intenção)

#caotico + periódico

# pega uma métrica (dtw) altera os valores de i
# e ve oq q da a forma da curva
# para cada i 1000 séries.
# envelope -- resultados possíveis para cada i

def plotResults():
    #data = pd.read_csv('dtwResults1.csv');
    #data2 = pd.read_csv('pearsonResultsR1.csv');
    data3 = pd.read_csv('miResults4.csv');

    fig = px.line(data3, x = 'Intensity', y = ['Average Distance', 'Min Distance', 'Max Distance'], title = 'Mutual Information (Intensity x Distance)');

    fig.show()


def calcI(serie1, serie2, dtwResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)

    dtwAlignment = ClassicMethods.calcDTW(s1Y, serie2.serieY, False)

    #ClassicMethods.plotSeries(s1X, s1Y);
    #ClassicMethods.plotSeries(serie2.serieX, serie2.serieY);

    dtwResults.append(dtwAlignment)

def calcPearson(serie1, serie2, pearsonResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    r, pValue = stats.pearsonr(s1Y, serie2.serieY)
    pearsonResults.append(r);

def calcMi(serie1, serie2, miResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    s2Y = copy(serie2.serieY);

    #s1Y = [int(num * 100000000) for num in s1Y];
    #s2Y = [int(num * 100000000) for num in s2Y];

    #pd.set_option("display.max_rows", 200, "display.max_columns", 3) 
    #print("out1")
    #cut, binsRuido = pd.cut(s1Y, 200, retbins=True);
    #out = pd.Series(cut).value_counts()
    #print(out)
    #print(len(out))
    
    #print("out2")
    #out2 = pd.Series(pd.cut(serie2.serieY, binsRuido)).value_counts();
    #print(out2)
    #print(len(out2))
    
    r = sm.mutual_info_score(s1Y, s2Y);   #1.5498260458782016

    #print("Mutual Info");
    #print(r);

    #print(s1Y)
    #print(s2Y)

    #ClassicMethods.plotSeries(s1X, s1Y);
    #ClassicMethods.plotSeries(serie2.serieX, s2Y);

    miResults.append(r);

def similaridadeXIntensidade(fileName, func): #pearson, mi, dtw
    serie1 = TS.TemporalSerie()
    serie2 = TS.TemporalSerie()

    results = []

    maxResults = []
    minResults = []
    averageResults = []

    iValues = np.linspace(0.001, 0.4, 400);  #(0.001, 0.4, 400) (0.01, 0.4, 40)

    serie1.genSineSerie(0, 30, 0.1, 5)
    serie2.genSineSerie(0, 30, 0.1, 5)

    for i in range(len(iValues)):
        for j in range(1000):
            func(serie1, serie2, results, iValues[i]);

        averageResults.append(np.mean(results));   
        maxResults.append(np.max(results));
        minResults.append(np.min(results));

        results = []

    f = open(fileName, "w+");
    writer = csv.writer(f);
    header = ['Intensity', 'Average Distance', 'Min Distance', 'Max Distance'];
    writer.writerow(header)

    for i in range(len(iValues)):
        data = [iValues[i], averageResults[i], minResults[i], maxResults[i]];
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
    #similaridadeXIntensidade("dtwResults1.csv", calcI)
    #similaridadeXIntensidade("pearsonResultsR1.csv", calcPearson)
    #similaridadeXIntensidade("miResults4.csv", calcMi);
    plotResults();
    
    
    #dtwAlignment = ClassicMethods.calcDTW(x1, x2);
    #print (dtwAlignment);
    #ClassicMethods.statisticalSignificance(x1, x2);

    pass


if __name__ == "__main__":
    main()
