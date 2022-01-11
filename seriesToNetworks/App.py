from random import randint
from re import X
import numpy
from scipy import*
import array
from numpy.lib.function_base import copy, piecewise
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
import sklearn.feature_selection._mutual_info as mmmi


#mutual information
#noise intensity
#quais características a comparação de séries através de redes
#podem capturar


def plotResults():
    #data = pd.read_csv('dtwResults1.csv');
    #data2 = pd.read_csv('pearsonResults.csv');
    #data3 = pd.read_csv('mi_4_neighbors.csv');

    allData = pd.read_csv('HD_DCTIF.csv');

    fig = px.line(allData, x = 'Intensity', y = ['Average Distance', 'Min Distance', 'Max Distance'], title = 'DCTIF -- Hamming distance');

    fig.show()


def calcI(serie1, serie2, dtwResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    dtwAlignment = ClassicMethods.calcDTW(s1Y, serie2.serieY, False)
    dtwResults.append(dtwAlignment)

def calcPearson(serie1, serie2, pearsonResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    r, pValue = stats.pearsonr(s1Y, serie2.serieY)
    pearsonResults.append(r);

def calcMi(serie1, serie2, miResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    
    #c_xy = np.histogram2d(s1Y, serie2.serieY, 8)[0]
    #mi = sm.mutual_info_score(None, None, contingency=c_xy)

    mi2 = mmmi._compute_mi_cc(s1Y, serie2.serieY, 4)   #k=4 || k=6

    #ClassicMethods.plotSeries(s1X, s1Y);
    #ClassicMethods.plotSeries(serie2.serieX, serie2.serieY);

    miResults.append(mi2);

def calcHd(adj_matrix, serie2, hdResults, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    
    graph2 = DCTIF();
    net2 = graph2.gen_network(s1Y)
    adj2 = net2.get_adjacency();

    len1 = adj_matrix.shape[0] * adj_matrix.shape[1]
    len2 = adj2.shape[0] * adj2.shape[1]

    minLen = None

    if len1 > len2:
        minLen = adj2
    else:
        minLen = adj_matrix

    max_adj = max([len1, len2])
    min_adj = min([len1, len2])

    diff = max_adj - min_adj

    countDiff = 0

    for i in range(minLen.shape[0]):
        for j in range(minLen.shape[1]):
            if(adj_matrix[i][j] != adj2[i][j]):
                countDiff += 1
    
    countDiff += diff

    hdResults.append(countDiff)   

def calcVG(adj_matrix, serie2, vg_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)

    graph2 = VG();
    net2 = graph2.gen_network(s1Y)
    adj2 = net2.get_adjacency();

    len1 = adj_matrix.shape[0] * adj_matrix.shape[1]
    len2 = adj2.shape[0] * adj2.shape[1]

    minLen = adj2

    if len1 > len2:
        minLen = adj2
    else:
        minLen = adj_matrix

    max_adj = max([len1, len2])
    min_adj = min([len1, len2])

    diff = max_adj - min_adj

    countDiff = 0

    for i in range(minLen.shape[0]):
        for j in range(minLen.shape[1]):
            if(adj_matrix[i][j] != adj2[i][j]):
                countDiff += 1
    
    countDiff += diff
    vg_results.append(countDiff)
   

def calcDCSD(adj_matrix, serie2, dcsd_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCSD()
    net2 = graph2.gen_network(s1Y)
    adj2 = net2

    len1 = adj_matrix.shape[0] * adj_matrix.shape[1]
    len2 = adj2.shape[0] * adj2.shape[1]

    minLen = adj2

    if len1 > len2:
        minLen = adj2
    else:
        minLen = adj_matrix

    max_adj = max([len1, len2])
    min_adj = min([len1, len2])

    diff = max_adj - min_adj

    countDiff = 0

    for i in range(minLen.shape[0]):
        for j in range(minLen.shape[1]):
            if(adj_matrix[i][j] != adj2[i][j]):
                countDiff += 1
    
    countDiff += diff
    
    dcsd_results.append(countDiff)
    

def network_similaridade_x_Intensidade(fileName, func): #pearson, mi, dtw
    serie1 = TS.TemporalSerie()
    serie2 = TS.TemporalSerie()

    results = []

    maxResults = []
    minResults = []
    averageResults = []

    iValues = np.linspace(0.001, 0.4, 400);  #(0.001, 0.4, 400) (0.01, 0.4, 40) (10, 4000, 400)

    serie1.genSineSerie(0, 30, 0.1, 5)
    serie2.genSineSerie(0, 30, 0.1, 5)

    graph1 = VG();
    net1 = graph1.gen_network(serie1.serieY);
    adj1 = net1.get_adjacency()

    for i in range(len(iValues)):
        for j in range(1000):
            func(adj1, serie2, results, iValues[i]);

        averageResults.append(np.mean(results));   
        maxResults.append(np.max(results));
        minResults.append(np.min(results));

        print(averageResults)
        print(maxResults)
        print(minResults)

        results = []

    f = open(fileName, "w+");
    writer = csv.writer(f);
    header = ['Intensity', 'Average Distance', 'Min Distance', 'Max Distance'];
    writer.writerow(header)

    for i in range(len(iValues)):
        data = [iValues[i], averageResults[i], minResults[i], maxResults[i]];
        writer.writerow(data);


def similaridadeXIntensidade(fileName, func): #pearson, mi, dtw
    serie1 = TS.TemporalSerie()
    serie2 = TS.TemporalSerie()

    results = []

    maxResults = []
    minResults = []
    averageResults = []

    iValues = np.linspace(0.001, 0.4, 400);  #(0.001, 0.4, 400) (0.01, 0.4, 40) (10, 4000, 400)

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

    #serie1.toFile("timeSerie1.txt");
    #serie2.toFile("timeSerie2.txt");

    #serie1.plotSeries()
    #serie2.plotSeries()

    #print(serie2.serieY)
    
    graphSin2 = DCSD()
    xxx = graphSin2.gen_network(serie2.serieY);

    print(xxx);
    #graphSin3 = VG("timeSerie1.txt");

    #graphSinNoise1 = DCTIF("timeSerie2.txt");
    #graphSinNoise2 = DCSD("timeSerie2.txt");
    #graphSinNoise3 = VG("timeSerie2.txt");


def testeRand():
    serietal = [0.1, 0.2, 0.7, 0.8, 0.2, 0.5]
    graph1 = VG();
    net1 = graph1.gen_network(serietal);
    

    # serie3.toFile("timeSeriesRand.txt");
    print(net1)


    #graphRand1 = DCTIF("timeSeriesRand.txt");
    #graphRand2 = DCSD("timeSeriesRand.txt");
    #graphRand3 = VG("timeSeriesRand.txt");


if __name__ == "__main__":
    #similaridadeXIntensidade("dtwResults.csv", calcI)
    #similaridadeXIntensidade("pearsonResults.csv", calcPearson)
    #similaridadeXIntensidade("miResults.csv", calcMi);
    
    #mergeResults()
    plotResults();
    
    #network_similaridade_x_Intensidade("HD_VG.csv", calcVG)
    
    #testeRand()
    #testeSin()